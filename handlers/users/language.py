from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.inline import get_language_keyboard
from utils.localization import get_message
from utils.db_api import user_repo

router = Router()


@router.message(Command("language"))
async def change_language(message: Message):
    """Change language command"""
    user = await user_repo.get_user(message.from_user.id)
    lang = user['language'] if user else 'ru'

    text = get_message(lang, 'start_greeting', name=message.from_user.full_name)
    await message.answer(text, reply_markup=get_language_keyboard())


@router.callback_query(F.data.startswith('lang_'))
async def update_language(callback: CallbackQuery):
    """Update user language"""
    language = callback.data.split('_')[1]

    await user_repo.update_language(callback.from_user.id, language)

    confirm_text = get_message(language, 'language_selected')
    await callback.message.edit_text(confirm_text)
    await callback.answer()
