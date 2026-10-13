import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from database import TriangleRepository


class TestTriangleRepository(unittest.TestCase):
    """Модульные тесты для БД (in-memory SQLite)."""

    def setUp(self):
        """Создаем свежую БД перед каждым тестом."""
        self.repo = TriangleRepository(":memory:")

    def tearDown(self):
        """Закрываем БД после каждого теста."""
        self.repo.close()

    def test_add_and_get_returns_saved_record(self):
        """После добавления запись можно получить."""
        self.repo.add(3.0, 4.0, 5.0, "разносторонний", "")
        result = self.repo.get(3.0, 4.0, 5.0)
        self.assertEqual(result, ("разносторонний", ""))

    def test_get_nonexistent_returns_none(self):
        """Получение несуществующей записи -> None."""
        result = self.repo.get(99.0, 99.0, 99.0)
        self.assertIsNone(result)

    def test_delete_removes_record(self):
        """Удаление убирает запись из БД."""
        self.repo.add(3.0, 4.0, 5.0, "разносторонний", "")
        deleted = self.repo.delete(3.0, 4.0, 5.0)
        self.assertTrue(deleted)
        self.assertIsNone(self.repo.get(3.0, 4.0, 5.0))

    def test_delete_nonexistent_returns_false(self):
        """Удаление несуществующей записи -> False."""
        deleted = self.repo.delete(99.0, 99.0, 99.0)
        self.assertFalse(deleted)

    def test_add_duplicate_replaces_record(self):
        """Повторное добавление той же записи обновляет её."""
        self.repo.add(3.0, 4.0, 5.0, "разносторонний", "")
        self.repo.add(3.0, 4.0, 5.0, "обновленный", "новое сообщение")
        result = self.repo.get(3.0, 4.0, 5.0)
        self.assertEqual(result, ("обновленный", "новое сообщение"))