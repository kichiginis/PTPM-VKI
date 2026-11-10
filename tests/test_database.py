import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from database import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):

    def setUp(self):
        self.repo = DatabaseRepository(":memory:")

    def tearDown(self):
        self.repo.close()

    # ============ add ============

    def test_add_success_returns_true(self):
        result = self.repo.add(1, "alice", "Hello world")
        self.assertTrue(result)

    def test_add_duplicate_id_returns_false(self):
        self.repo.add(1, "alice", "First message")
        result = self.repo.add(1, "bob", "Second message")
        self.assertFalse(result)

    def test_add_name_too_long_returns_false(self):
        long_name = "a" * 300  # > 256
        result = self.repo.add(1, long_name, "msg")
        self.assertFalse(result)

    def test_add_message_too_long_returns_false(self):
        long_msg = "x" * 9000  # > 8096
        result = self.repo.add(1, "alice", long_msg)
        self.assertFalse(result)

    def test_add_non_int_id_returns_false(self):
        result = self.repo.add("not_int", "alice", "msg")
        self.assertFalse(result)

    # ============ get_by_id ============

    def test_get_by_id_existing_returns_dict(self):
        self.repo.add(1, "alice", "Hello")
        result = self.repo.get_by_id(1)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "alice")
        self.assertEqual(result["message"], "Hello")

    def test_get_by_id_nonexistent_returns_none(self):
        result = self.repo.get_by_id(999)
        self.assertIsNone(result)

    # ============ get_by_name ============

    def test_get_by_name_multiple_returns_list(self):
        self.repo.add(1, "alice", "First")
        self.repo.add(2, "alice", "Second")
        self.repo.add(3, "bob", "Third")
        result = self.repo.get_by_name("alice")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["message"], "First")
        self.assertEqual(result[1]["message"], "Second")

    def test_get_by_name_nonexistent_returns_empty_list(self):
        result = self.repo.get_by_name("nobody")
        self.assertEqual(result, [])

    # ============ update ============

    def test_update_existing_returns_true_and_changes_message(self):
        self.repo.add(1, "alice", "Old message")
        result = self.repo.update(1, "New message")
        self.assertTrue(result)
        self.assertEqual(self.repo.get_by_id(1)["message"], "New message")

    def test_update_nonexistent_returns_false(self):
        result = self.repo.update(999, "New message")
        self.assertFalse(result)

    def test_update_message_too_long_returns_false(self):
        self.repo.add(1, "alice", "Short")
        result = self.repo.update(1, "x" * 9000)
        self.assertFalse(result)

    # ============ delete ============

    def test_delete_existing_returns_true(self):
        self.repo.add(1, "alice", "Hello")
        result = self.repo.delete(1)
        self.assertTrue(result)
        self.assertIsNone(self.repo.get_by_id(1))

    def test_delete_nonexistent_returns_false(self):
        result = self.repo.delete(999)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()