from aiogram import Router

from . import help
from . import start
from . import language
from . import chess_analysis
from . import echo


def setup_routers() -> Router:
    router = Router()

    # Order matters - more specific handlers first
    router.include_router(start.router)
    router.include_router(help.router)
    router.include_router(language.router)
    router.include_router(chess_analysis.router)
    router.include_router(echo.router)  # Last - catches everything else

    return router
