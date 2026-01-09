from utils.db_api.database import db


class AnalysisRepository:
    async def create_analysis(
        self,
        user_id: int,
        fen: str,
        best_move: str,
        evaluation: float,
        explanation: str
    ) -> int:
        """Save chess analysis"""
        cursor = await db.connection.execute(
            """
            INSERT INTO analyses (user_id, fen, best_move, evaluation, explanation)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, fen, best_move, evaluation, explanation)
        )
        await db.connection.commit()
        return cursor.lastrowid

    async def get_user_analyses_count(self, user_id: int) -> int:
        """Get total analyses count for user"""
        cursor = await db.connection.execute(
            "SELECT COUNT(*) as count FROM analyses WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        return row['count'] if row else 0


analysis_repo = AnalysisRepository()
