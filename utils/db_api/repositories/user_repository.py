from typing import Optional
from utils.db_api.database import db


class UserRepository:
    async def get_user(self, telegram_id: int) -> Optional[dict]:
        """Get user by telegram_id"""
        cursor = await db.connection.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def create_user(self, telegram_id: int, language: str = 'ru') -> int:
        """Create new user"""
        cursor = await db.connection.execute(
            "INSERT INTO users (telegram_id, language) VALUES (?, ?)",
            (telegram_id, language)
        )
        await db.connection.commit()
        return cursor.lastrowid

    async def update_language(self, telegram_id: int, language: str):
        """Update user language preference"""
        await db.connection.execute(
            "UPDATE users SET language = ? WHERE telegram_id = ?",
            (language, telegram_id)
        )
        await db.connection.commit()

    async def get_or_create_user(self, telegram_id: int, language: str = 'ru') -> dict:
        """Get existing user or create new one"""
        user = await self.get_user(telegram_id)
        if not user:
            user_id = await self.create_user(telegram_id, language)
            user = await self.get_user(telegram_id)
        return user


user_repo = UserRepository()
