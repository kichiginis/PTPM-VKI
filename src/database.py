import sqlite3


class TriangleRepository:
    """Репозиторий для работы с БД SQLite."""

    def __init__(self, db_path=":memory:"):
        """
        :param db_path: путь к файлу БД. По умолчанию — in-memory (для тестов).
        """
        self.connection = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                side_a REAL,
                side_b REAL,
                side_c REAL,
                tri_type TEXT,
                error_message TEXT,
                PRIMARY KEY (side_a, side_b, side_c)
            )
        """)
        self.connection.commit()

    def add(self, side_a, side_b, side_c, tri_type, error_message):
        """Добавляет запись. Если такая уже есть — обновляет."""
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO triangles 
            (side_a, side_b, side_c, tri_type, error_message)
            VALUES (?, ?, ?, ?, ?)
        """, (side_a, side_b, side_c, tri_type, error_message))
        self.connection.commit()

    def get(self, side_a, side_b, side_c):
        """Возвращает запись или None, если её нет."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT tri_type, error_message FROM triangles
            WHERE side_a = ? AND side_b = ? AND side_c = ?
        """, (side_a, side_b, side_c))
        return cursor.fetchone()

    def delete(self, side_a, side_b, side_c):
        """Удаляет запись. Возвращает True, если что-то удалили."""
        cursor = self.connection.cursor()
        cursor.execute("""
            DELETE FROM triangles
            WHERE side_a = ? AND side_b = ? AND side_c = ?
        """, (side_a, side_b, side_c))
        self.connection.commit()
        return cursor.rowcount > 0

    def close(self):
        self.connection.close()