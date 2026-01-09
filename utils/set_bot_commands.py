from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_commands(bot: Bot):
    """Set bot commands in menu"""
    commands = [
        BotCommand(command="start", description="Начать работу / Ishni boshlash"),
        BotCommand(command="help", description="Помощь / Yordam"),
        BotCommand(command="language", description="Сменить язык / Tilni o'zgartirish"),
    ]

    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
