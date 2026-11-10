import sqlite3


class DatabaseRepository:
    """Репозиторий для работы с таблицей comments в SQLite."""

    def __init__(self, db_path=":memory:"):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row  # <-- доступ по имени колонки
        self._create_table()

    def _create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL CHECK(length(name) <= 256),
                message TEXT NOT NULL CHECK(length(message) <= 8096)
            )
        """)
        self.connection.commit()

    def add(self, comment_id: int, username: str, message: str) -> bool:
        """Добавляет запись. Возвращает True при успехе, False при ошибке."""
        # Валидация типов
        if not isinstance(comment_id, int) or not isinstance(username, str) or not isinstance(message, str):
            return False

        # Валидация длины
        if len(username) > 256 or len(message) > 8096:
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                (comment_id, username, message)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            # Дублирование ID
            return False

    def get_by_id(self, comment_id: int):
        """Возвращает запись по ID или None."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM comments WHERE id = ?", (comment_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    def get_by_name(self, username: str) -> list:
        """Возвращает список всех записей пользователя."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM comments WHERE name = ?", (username,))
        return [dict(row) for row in cursor.fetchall()]

    def update(self, comment_id: int, new_message: str) -> bool:
        """Обновляет message по ID. Возвращает True, если запись была обновлена."""
        if not isinstance(new_message, str) or len(new_message) > 8096:
            return False

        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE comments SET message = ? WHERE id = ?",
            (new_message, comment_id)
        )
        self.connection.commit()
        return cursor.rowcount > 0  # True, если строка была найдена

    def delete(self, comment_id: int) -> bool:
        """Удаляет запись. Возвращает True, если что-то удалили."""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    def close(self):
        self.connection.close()