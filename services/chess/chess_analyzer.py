from typing import Dict, Optional
import logging
from .gemini_vision_service import gemini_vision
from .stockfish_service import stockfish_service
from .gemini_text_service import gemini_text
from utils.db_api import analysis_repo
from utils.localization import get_message

logger = logging.getLogger(__name__)


class ChessAnalyzer:
    """
    Orchestrates the full chess analysis pipeline:
    1. Image → FEN (Gemini Vision)
    2. FEN → Best move + evaluation (Stockfish)
    3. Generate explanation (Gemini Text)
    4. Save to database
    """

    async def analyze_image(
        self,
        image_bytes: bytes,
        user_id: int,
        language: str = 'ru'
    ) -> Optional[Dict]:
        """
        Full analysis pipeline

        Returns:
            Dict with analysis results or Dict with error key if failed
        """
        try:
            # Step 1: Recognize position
            fen = await gemini_vision.image_to_fen(image_bytes)
            if not fen:
                return {'error': 'no_board'}

            # Step 2: Analyze with Stockfish
            analysis = await stockfish_service.analyze_position(fen)
            if not analysis:
                return {'error': 'invalid_fen'}

            # Step 3: Generate explanation
            explanation = await gemini_text.explain_move(
                fen=fen,
                best_move=analysis['best_move'],
                evaluation=analysis['evaluation_value'],
                language=language
            )

            if not explanation:
                explanation = self._get_fallback_explanation(language)

            # Step 4: Format evaluation
            evaluation_text = self._format_evaluation(
                analysis['evaluation_type'],
                analysis['evaluation_value'],
                language
            )

            # Step 5: Save to database
            await analysis_repo.create_analysis(
                user_id=user_id,
                fen=fen,
                best_move=analysis['best_move'],
                evaluation=analysis['evaluation_value'] if analysis['evaluation_type'] == 'cp' else None,
                explanation=explanation
            )

            return {
                'fen': fen,
                'best_move': analysis['best_move'],
                'evaluation': evaluation_text,
                'explanation': explanation
            }

        except Exception as e:
            logger.error(f"Analysis pipeline error: {e}")
            return {'error': 'general'}

    def _format_evaluation(self, eval_type: str, eval_value: int, language: str) -> str:
        """Format evaluation as human-readable text"""
        if eval_type == 'mate':
            return get_message(language, 'eval_mate_in', moves=abs(eval_value))

        # Convert centipawns to pawns
        eval_pawns = eval_value / 100

        if eval_pawns > 3:
            return f"+{eval_pawns:.1f} {get_message(language, 'eval_white_winning')}"
        elif eval_pawns > 0.5:
            return f"+{eval_pawns:.1f} {get_message(language, 'eval_white_advantage')}"
        elif eval_pawns > -0.5:
            return f"{eval_pawns:+.1f} {get_message(language, 'eval_equal')}"
        elif eval_pawns > -3:
            return f"{eval_pawns:.1f} {get_message(language, 'eval_black_advantage')}"
        else:
            return f"{eval_pawns:.1f} {get_message(language, 'eval_black_winning')}"

    def _get_fallback_explanation(self, language: str) -> str:
        """Fallback explanation if Gemini fails"""
        if language == 'uz':
            return "• eng yaxshi yurish\n• pozitsiyani yaxshilaydi"
        return "• лучший ход в позиции\n• улучшает позицию"


chess_analyzer = ChessAnalyzer()
