from google import genai
from google.genai import types
from data import config
import logging
from typing import Optional
from PIL import Image
import io
import base64

logger = logging.getLogger(__name__)


class GeminiVisionService:
    def __init__(self):
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)

    async def image_to_fen(self, image_bytes: bytes) -> Optional[str]:
        """
        Convert chess board image to FEN notation

        Args:
            image_bytes: Image file bytes

        Returns:
            FEN string or None if recognition failed
        """
        try:
            prompt = """
Analyze this chess board image and provide the position in FEN (Forsyth-Edwards Notation) format.

Requirements:
1. Return ONLY the FEN string, nothing else
2. Include all 6 FEN components: piece placement, active color, castling, en passant, halfmove, fullmove
3. If the board is unclear or you cannot identify it, return "ERROR: unclear board"
4. Standard starting position example: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

Return only the FEN string, no other text.
"""

            # Encode image to base64
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

            # Generate content
            response = self.client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[
                    types.Part.from_text(text=prompt),
                    types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg')
                ]
            )

            fen = response.text.strip()

            # Basic validation
            if "ERROR" in fen or not fen:
                logger.warning("Gemini could not recognize board")
                return None

            logger.info(f"Recognized FEN: {fen}")
            return fen

        except Exception as e:
            logger.error(f"Gemini Vision API error: {e}")
            return None


gemini_vision = GeminiVisionService()
