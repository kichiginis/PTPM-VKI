import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from parser import ForumParser
from database import DatabaseRepository

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "quotes_page.html")


class TestForumParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Читаем фикстуру один раз для всех тестов."""
        if not os.path.exists(FIXTURE_PATH):
            raise FileNotFoundError(
                f"Фикстура не найдена: {FIXTURE_PATH}. Сохраните страницу вручную."
            )
        with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
            cls.html = f.read()

    def setUp(self):
        self.parser = ForumParser()

    # ============ parse_html ============

    def test_parse_html_returns_non_empty_list(self):
        result = self.parser.parse_html(self.html)
        self.assertGreater(len(result), 0)

    def test_parse_html_first_item_has_correct_fields(self):
        result = self.parser.parse_html(self.html)
        first = result[0]
        self.assertIn("id", first)
        self.assertIn("name", first)
        self.assertIn("message", first)

    def test_parse_html_id_is_int(self):
        result = self.parser.parse_html(self.html)
        for item in result:
            self.assertIsInstance(item["id"], int)

    def test_parse_html_known_author_present(self):
        """Известный факт: на главной странице есть цитаты Albert Einstein."""
        result = self.parser.parse_html(self.html)
        names = [item["name"] for item in result]
        self.assertIn("Albert Einstein", names)

    def test_parse_html_known_text_present(self):
        """Известный факт: на странице есть цитата про 'The world as we have created it'."""
        result = self.parser.parse_html(self.html)
        messages = [item["message"] for item in result]
        found = any("The world as we have created it" in m for m in messages)
        self.assertTrue(found)

    # ============ save_to_db ============

    def test_save_to_db_inserts_records(self):
        result = self.parser.parse_html(self.html)
        repo = DatabaseRepository(":memory:")
        added = self.parser.save_to_db(result, repo)
        self.assertEqual(added, len(result))

        # Проверяем, что первая запись есть в БД
        first = result[0]
        saved = repo.get_by_id(first["id"])
        self.assertIsNotNone(saved)
        self.assertEqual(saved["name"], first["name"])
        repo.close()


if __name__ == '__main__':
    unittest.main()