from aiogram import Router, F
from aiogram.types import Message, PhotoSize
import logging

from utils.localization import get_message
from utils.db_api import user_repo
from services import chess_analyzer
from data import config

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.photo)
async def handle_chess_image(message: Message):
    """Handle chess board photo"""
    # Get user and language
    user = await user_repo.get_or_create_user(message.from_user.id)
    lang = user['language']

    # Show processing message
    processing_msg = await message.answer(get_message(lang, 'processing'))

    try:
        # Get largest photo
        photo: PhotoSize = message.photo[-1]

        # Validate file size
        if photo.file_size > config.MAX_IMAGE_SIZE_MB * 1024 * 1024:
            await processing_msg.edit_text(get_message(lang, 'error_image_too_large'))
            return

        # Download photo
        file = await message.bot.download(photo.file_id)
        image_bytes = file.read()

        # Analyze chess position
        result = await chess_analyzer.analyze_image(
            image_bytes=image_bytes,
            user_id=user['id'],
            language=lang
        )

        # Handle errors
        if not result or 'error' in result:
            error_key = f"error_{result.get('error', 'general')}"
            error_text = get_message(lang, error_key)
            await processing_msg.edit_text(error_text)
            return

        # Format result
        response_text = get_message(
            lang,
            'analysis_result',
            move=result['best_move'],
            evaluation=result['evaluation'],
            explanation=result['explanation']
        )

        await processing_msg.edit_text(response_text)

    except Exception as e:
        logger.error(f"Chess analysis handler error: {e}")
        await processing_msg.edit_text(get_message(lang, 'error_general'))
