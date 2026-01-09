from stockfish import Stockfish
from data import config
import logging
from typing import Dict, Optional
import chess
import os

logger = logging.getLogger(__name__)


class StockfishService:
    def __init__(self):
        # Try to find Stockfish binary
        stockfish_path = self._find_stockfish_binary()

        # Stockfish library configuration
        self.stockfish = Stockfish(
            path=stockfish_path,
            depth=config.STOCKFISH_DEPTH,
            parameters={
                "Threads": 2,
                "Minimum Thinking Time": 100,
            }
        )

    def _find_stockfish_binary(self) -> str:
        """Find Stockfish binary path"""
        # Get project root directory (go up 3 levels from this file)
        # This file: services/chess/stockfish_service.py
        # Project root: ../../../
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))

        # Common installation paths
        paths = [
            os.path.join(project_root, 'bin/stockfish/stockfish-macos-m1-apple-silicon'),  # Local download Apple Silicon
            os.path.join(project_root, 'bin/stockfish/stockfish-macos-x86-64-avx2'),  # Local download Intel
            '/opt/homebrew/bin/stockfish',  # Homebrew on Apple Silicon
            '/usr/local/bin/stockfish',  # Homebrew on Intel Mac
            '/usr/bin/stockfish',  # Linux apt
            '/usr/games/stockfish',  # Linux games
        ]

        for path in paths:
            if os.path.exists(path):
                logger.info(f"Found Stockfish at: {path}")
                return path

        # Debug: show what we tried
        logger.error(f"Project root: {project_root}")
        logger.error(f"Tried paths: {paths}")

        raise FileNotFoundError(
            "Stockfish not found. Please install it:\n"
            "macOS: brew install stockfish\n"
            "Linux: sudo apt-get install stockfish\n"
            "Or download from: https://stockfishchess.org/download/"
        )

    async def analyze_position(self, fen: str) -> Optional[Dict]:
        """
        Analyze chess position

        Args:
            fen: Position in FEN notation

        Returns:
            Dict with best_move, evaluation_type, evaluation_value
        """
        try:
            # Validate FEN using python-chess
            try:
                board = chess.Board(fen)
            except ValueError as e:
                logger.error(f"Invalid FEN: {fen} - {e}")
                return None

            # Set position
            self.stockfish.set_fen_position(fen)

            # Get best move
            best_move = self.stockfish.get_best_move_time(
                int(config.STOCKFISH_TIME_LIMIT * 1000)
            )

            if not best_move:
                logger.warning("Stockfish returned no best move")
                return None

            # Get evaluation
            evaluation = self.stockfish.get_evaluation()

            # Convert UCI move to SAN notation
            move_obj = chess.Move.from_uci(best_move)
            san_move = board.san(move_obj)

            result = {
                'best_move': san_move,
                'best_move_uci': best_move,
                'evaluation_type': evaluation['type'],  # 'cp' or 'mate'
                'evaluation_value': evaluation['value']
            }

            logger.info(f"Analysis: {result}")
            return result

        except Exception as e:
            logger.error(f"Stockfish analysis error: {e}")
            return None


stockfish_service = StockfishService()
