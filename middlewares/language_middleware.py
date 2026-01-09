from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from utils.db_api import user_repo


class LanguageMiddleware(BaseMiddleware):
    """Inject user language preference into handler context"""

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Get user from database
        user = await user_repo.get_user(event.from_user.id)

        # Add language to handler data
        data['user_language'] = user['language'] if user else 'ru'
        data['user_db'] = user

        return await handler(event, data)
