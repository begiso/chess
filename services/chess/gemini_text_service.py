from google import genai
from google.genai import types
from data import config
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class GeminiTextService:
    def __init__(self):
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)

    async def explain_move(
        self,
        fen: str,
        best_move: str,
        evaluation: float,
        language: str = 'ru'
    ) -> Optional[str]:
        """
        Generate move explanation in specified language

        Args:
            fen: Position in FEN notation
            best_move: Best move in SAN notation
            evaluation: Position evaluation
            language: 'ru' or 'uz'

        Returns:
            Explanation text with bullet points
        """
        try:
            lang_instruction = {
                'ru': 'на русском языке',
                'uz': 'на узбекском языке (o\'zbek tilida)'
            }

            prompt = f"""
Ты шахматный тренер. Объясни {lang_instruction.get(language, 'на русском языке')}, почему ход {best_move} является лучшим в этой позиции.

FEN позиции: {fen}
Лучший ход: {best_move}
Оценка: {evaluation}

Требования к ответу:
1. Дай краткое объяснение (2-4 пункта)
2. Используй маркированный список с символом •
3. Объясни стратегическую или тактическую идею
4. Будь конкретным и понятным
5. НЕ используй слишком технический жаргон

Пример формата:
• развитие фигуры на активную позицию
• контроль центра
• подготовка к рокировке

Верни только список с пунктами, без дополнительного текста.
"""

            response = self.client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )

            explanation = response.text.strip()

            logger.info(f"Generated explanation ({language}): {explanation[:100]}...")
            return explanation

        except Exception as e:
            logger.error(f"Gemini Text API error: {e}")
            return None


gemini_text = GeminiTextService()
