from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .language_middleware import LanguageMiddleware


def setup_middlewares(dp: Dispatcher):
    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(LanguageMiddleware())
