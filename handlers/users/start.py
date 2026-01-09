from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.inline import get_language_keyboard
from utils.localization import get_message
from utils.db_api import user_repo
from states import LanguageSelection

router = Router()


@router.message(CommandStart())
async def bot_start(message: Message, state: FSMContext):
    """Start command - show language selection"""
    user = await user_repo.get_user(message.from_user.id)

    if user:
        # Existing user - greet in their language
        lang = user['language']
        text = get_message(lang, 'help_text')
        await message.answer(text)
    else:
        # New user - ask for language
        text = get_message('ru', 'start_greeting', name=message.from_user.full_name)
        await message.answer(text, reply_markup=get_language_keyboard())
        await state.set_state(LanguageSelection.waiting_for_language)


@router.callback_query(F.data.startswith('lang_'))
async def language_selected(callback: CallbackQuery, state: FSMContext):
    """Handle language selection"""
    language = callback.data.split('_')[1]  # lang_ru → ru

    # Save user with selected language
    await user_repo.get_or_create_user(callback.from_user.id, language)

    # Show confirmation and help
    confirm_text = get_message(language, 'language_selected')
    help_text = get_message(language, 'help_text')

    await callback.message.edit_text(confirm_text)
    await callback.message.answer(help_text)
    await state.clear()
    await callback.answer()
