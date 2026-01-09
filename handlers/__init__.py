from aiogram import Router

from . import errors
from . import users
# from . import groups
# from . import channels


def setup_routers() -> Router:
    router = Router()
    
    # Подключаем роутеры
    router.include_router(users.setup_routers())
    
    return router
