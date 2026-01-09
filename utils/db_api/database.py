import aiosqlite
from typing import Optional
from data import config
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str = config.DB_PATH):
        self.db_path = db_path
        self.connection: Optional[aiosqlite.Connection] = None

    async def connect(self):
        """Establish database connection"""
        self.connection = await aiosqlite.connect(self.db_path)
        self.connection.row_factory = aiosqlite.Row
        logger.info(f"Database connected: {self.db_path}")

    async def disconnect(self):
        """Close database connection"""
        if self.connection:
            await self.connection.close()
            logger.info("Database disconnected")

    async def create_tables(self):
        """Create database schema"""
        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                language TEXT NOT NULL DEFAULT 'ru',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                fen TEXT NOT NULL,
                best_move TEXT NOT NULL,
                evaluation REAL,
                explanation TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        await self.connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_telegram_id
            ON users(telegram_id)
        """)

        await self.connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_analyses_user_id
            ON analyses(user_id)
        """)

        await self.connection.commit()
        logger.info("Database tables created")


# Global database instance
db = Database()
