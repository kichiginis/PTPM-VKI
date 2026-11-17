import unittest
import os
from src.parser import ForumParser
from src.database import DatabaseRepository


class TestForumParser(unittest.TestCase):
    def setUp(self):
        self.parser = ForumParser()
        # Путь к фикстуре относительно текущего файла теста
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.fixture_path = os.path.join(current_dir, 'fixtures', 'fixture_cyberforum.html')

    def test_parse_file_extracts_posts_correctly(self):
        """Тест 1: Проверка базового извлечения постов"""
        posts = self.parser.parse_file(self.fixture_path)

        # На странице минимум 3 поста (1 вопрос и 2 ответа)
        self.assertGreaterEqual(len(posts), 3)

        # Проверка первого поста (вопрос от Obel)
        first_post = posts[0]
        self.assertEqual(first_post['id'], 15190304)
        self.assertEqual(first_post['name'], 'Obel')
        self.assertIn('Market', first_post['message'])

    def test_parse_file_preserves_html_markup(self):
        """Тест 2: Проверка сохранения HTML-разметки в сообщениях"""
        posts = self.parser.parse_file(self.fixture_path)

        # Проверка второго поста (ответ от vrm2, содержит блоки кода)
        second_post = posts[1]
        self.assertEqual(second_post['id'], 15191121)
        self.assertEqual(second_post['name'], 'vrm2')
        # Проверяем, что HTML-разметка (теги) сохранилась
        self.assertIn('<div class="codeblock">', second_post['message'])
        self.assertIn('<pre class="de1">', second_post['message'])

    def test_save_to_db_integration(self):
        """Тест 3: Интеграционный тест сохранения в БД"""
        posts = self.parser.parse_file(self.fixture_path)
        repo = DatabaseRepository(':memory:')

        saved_count = self.parser.save_to_db(posts, repo)

        self.assertEqual(saved_count, len(posts))
        # Проверяем, что данные действительно попали в БД
        db_record = repo.get_by_id(15192304)  # ID третьего поста (Shamil1)
        self.assertIsNotNone(db_record)
        self.assertEqual(db_record['name'], 'Shamil1')

    def test_parse_file_returns_correct_post_count(self):
        """Тест 4: Проверка точного количества постов на странице"""
        posts = self.parser.parse_file(self.fixture_path)

        # На данной странице ровно 3 поста
        self.assertEqual(len(posts), 3)

    def test_parse_file_all_posts_have_valid_ids(self):
        """Тест 5: Проверка корректности ID всех постов"""
        posts = self.parser.parse_file(self.fixture_path)

        expected_ids = [15190304, 15191121, 15192304]
        actual_ids = [post['id'] for post in posts]

        self.assertEqual(actual_ids, expected_ids)
        # Все ID должны быть целыми числами
        for post in posts:
            self.assertIsInstance(post['id'], int)
            self.assertGreater(post['id'], 0)

    def test_parse_file_all_posts_have_valid_authors(self):
        """Тест 6: Проверка корректности имен авторов"""
        posts = self.parser.parse_file(self.fixture_path)

        expected_authors = ['Obel', 'vrm2', 'Shamil1']
        actual_authors = [post['name'] for post in posts]

        self.assertEqual(actual_authors, expected_authors)
        # Все имена должны быть непустыми строками
        for post in posts:
            self.assertIsInstance(post['name'], str)
            self.assertGreater(len(post['name']), 0)

    def test_parse_file_all_posts_have_non_empty_messages(self):
        """Тест 7: Проверка, что все сообщения непустые"""
        posts = self.parser.parse_file(self.fixture_path)

        for post in posts:
            self.assertIsInstance(post['message'], str)
            self.assertGreater(len(post['message']), 0)

    def test_parse_file_raises_on_nonexistent_file(self):
        """Тест 8: Проверка обработки несуществующего файла"""
        nonexistent_path = 'tests/fixtures/nonexistent_file.html'

        with self.assertRaises(FileNotFoundError):
            self.parser.parse_file(nonexistent_path)

    def test_save_to_db_returns_correct_count(self):
        """Тест 9: Проверка возвращаемого количества сохраненных записей"""
        posts = self.parser.parse_file(self.fixture_path)
        repo = DatabaseRepository(':memory:')

        saved_count = self.parser.save_to_db(posts, repo)

        # Должно сохраниться ровно 3 поста
        self.assertEqual(saved_count, 3)

    def test_save_to_db_handles_duplicates_gracefully(self):
        """Тест 10: Проверка корректной обработки дубликатов при сохранении"""
        posts = self.parser.parse_file(self.fixture_path)
        repo = DatabaseRepository(':memory:')

        # Сохраняем первый раз
        first_save_count = self.parser.save_to_db(posts, repo)
        self.assertEqual(first_save_count, 3)

        # Сохраняем второй раз (те же данные) - дубликаты должны игнорироваться
        second_save_count = self.parser.save_to_db(posts, repo)
        self.assertEqual(second_save_count, 0)  # Ничего не сохранилось, т.к. все дубликаты

        # Проверяем, что в БД все еще 3 записи (не 6)
        all_records = []
        for post_id in [15190304, 15191121, 15192304]:
            record = repo.get_by_id(post_id)
            if record:
                all_records.append(record)

        self.assertEqual(len(all_records), 3)


if __name__ == '__main__':
    unittest.main()