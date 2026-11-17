import sqlite3
from typing import Optional, List, Dict, Any

class DatabaseRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path
        # Храним одно соединение на экземпляр класса.
        # Это критически важно для корректной работы с ':memory:'
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL CHECK(LENGTH(name) <= 256),
                message TEXT NOT NULL CHECK(LENGTH(message) <= 8096)
            )
        """)
        self.conn.commit()

    def add(self, comment_id: int, username: str, message: str) -> bool:
        if not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть целым числом (int)")
        if not isinstance(username, str) or not isinstance(message, str):
            raise TypeError("username и message должны быть строками (str)")
        if len(username) > 256:
            raise ValueError("Длина username не может превышать 256 символов")
        if len(message) > 8096:
            raise ValueError("Длина message не может превышать 8096 символов")

        try:
            self.conn.execute(
                "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                (comment_id, username, message)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            raise ValueError(f"Запись с comment_id={comment_id} уже существует")

    def get_by_id(self, comment_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT id, name, message FROM comments WHERE id = ?", (comment_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_by_name(self, username: str) -> List[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT id, name, message FROM comments WHERE name = ?", (username,))
        return [dict(row) for row in cursor.fetchall()]

    def update(self, comment_id: int, new_message: str) -> bool:
        if not isinstance(new_message, str):
            raise TypeError("new_message должен быть строкой (str)")
        if len(new_message) > 8096:
            raise ValueError("Длина new_message не может превышать 8096 символов")

        cursor = self.conn.execute(
            "UPDATE comments SET message = ? WHERE id = ?",
            (new_message, comment_id)
        )
        self.conn.commit()
        if cursor.rowcount == 0:
            raise ValueError(f"Запись с comment_id={comment_id} не найдена")
        return True

    def delete(self, comment_id: int) -> bool:
        cursor = self.conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        self.conn.commit()
        if cursor.rowcount == 0:
            raise ValueError(f"Запись с comment_id={comment_id} не найдена")
        return True

    def close(self):
        """Метод для явного закрытия соединения (хорошая практика)"""
        self.conn.close()