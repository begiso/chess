from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.localization import MESSAGES


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Create language selection keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=MESSAGES['ru']['btn_russian'],
                callback_data='lang_ru'
            )
        ],
        [
            InlineKeyboardButton(
                text=MESSAGES['uz']['btn_uzbek'],
                callback_data='lang_uz'
            )
        ]
    ])
    return keyboard
