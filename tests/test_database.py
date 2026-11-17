import unittest
import sqlite3
from src.database import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):
    def setUp(self):
        # Используем базу данных в памяти для изоляции тестов
        self.repo = DatabaseRepository(':memory:')

    def test_add_success(self):
        result = self.repo.add(1, 'user1', 'Hello World')
        self.assertTrue(result)
        self.assertEqual(self.repo.get_by_id(1)['name'], 'user1')

    def test_add_duplicate_id_raises(self):
        self.repo.add(1, 'user1', 'First message')
        with self.assertRaises(ValueError):
            self.repo.add(1, 'user2', 'Duplicate message')

    def test_add_invalid_length_raises(self):
        with self.assertRaises(ValueError):
            self.repo.add(2, 'u' * 257, 'Valid message')

    def test_get_by_id_success(self):
        self.repo.add(10, 'alice', 'Test message')
        record = self.repo.get_by_id(10)
        self.assertEqual(record['id'], 10)
        self.assertEqual(record['name'], 'alice')

    def test_get_by_id_not_found(self):
        self.assertIsNone(self.repo.get_by_id(999))

    def test_get_by_name_success(self):
        self.repo.add(1, 'bob', 'Message 1')
        self.repo.add(2, 'bob', 'Message 2')
        self.repo.add(3, 'alice', 'Message 3')

        records = self.repo.get_by_name('bob')
        self.assertEqual(len(records), 2)
        self.assertTrue(all(r['name'] == 'bob' for r in records))

    def test_update_success(self):
        self.repo.add(5, 'charlie', 'Old message')
        result = self.repo.update(5, 'New updated message')
        self.assertTrue(result)
        self.assertEqual(self.repo.get_by_id(5)['message'], 'New updated message')

    def test_update_not_found_raises(self):
        with self.assertRaises(ValueError):
            self.repo.update(888, 'This should fail')

    def test_delete_success(self):
        self.repo.add(7, 'dave', 'To be deleted')
        result = self.repo.delete(7)
        self.assertTrue(result)
        self.assertIsNone(self.repo.get_by_id(7))

    def test_delete_not_found_raises(self):
        with self.assertRaises(ValueError):
            self.repo.delete(777)


if __name__ == '__main__':
    unittest.main()