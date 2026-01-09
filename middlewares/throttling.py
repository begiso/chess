from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware для защиты от флуда (aiogram 3.x)
    """
    def __init__(self, time_limit: int = 2):
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        
        if user_id in self.limit:
            return await event.answer("Too many requests!")
        else:
            self.limit[user_id] = None
        
        return await handler(event, data)
