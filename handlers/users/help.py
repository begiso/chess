from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils.localization import get_message
from utils.db_api import user_repo

router = Router()


@router.message(Command("help"))
async def bot_help(message: Message):
    """Help command with localization"""
    user = await user_repo.get_user(message.from_user.id)
    lang = user['language'] if user else 'ru'

    text = get_message(lang, 'help_text')
    await message.answer(text)
