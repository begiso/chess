from aiogram import Router
from aiogram.types import Message
from aiogram import F

from utils.localization import get_message
from utils.db_api import user_repo

router = Router()


# Remind user to send photos instead of echoing text
@router.message(F.text)
async def bot_echo(message: Message):
    """Remind user to send chess board photos"""
    user = await user_repo.get_user(message.from_user.id)
    lang = user['language'] if user else 'ru'

    await message.answer(get_message(lang, 'help_text'))
