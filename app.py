import asyncio
import logging

from aiogram import Bot

from loader import dp, bot
from handlers import setup_routers
from handlers.errors import error_handler
from middlewares import setup_middlewares
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api import db


async def on_startup(bot: Bot):
    # Initialize database
    await db.connect()
    await db.create_tables()

    # Set bot commands
    await set_default_commands(bot)

    # Notify admin
    await on_startup_notify(bot)


async def on_shutdown(bot: Bot):
    # Close database connection
    await db.disconnect()


async def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Setup middlewares
    setup_middlewares(dp)

    # Setup handlers
    dp.include_router(setup_routers())

    # Setup error handler
    dp.include_router(error_handler.router)

    # Startup
    await on_startup(bot)

    try:
        # Start polling
        await dp.start_polling(bot)
    finally:
        # Shutdown
        await on_shutdown(bot)


if __name__ == '__main__':
    asyncio.run(main())
