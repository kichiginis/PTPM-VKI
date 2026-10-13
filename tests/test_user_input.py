import unittest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from user_input import ConsoleUserInput


class TestConsoleUserInput(unittest.TestCase):
    """Тесты для класса ConsoleUserInput с подменой input()."""

    @patch('builtins.input', side_effect=["3", "4", "5"])
    def test_get_sides_reads_three_values(self, mock_input):
        """Проверяем, что input() вызывается 3 раза и возвращает данные."""
        ui = ConsoleUserInput()
        a, b, c = ui.get_sides()

        self.assertEqual((a, b, c), ("3", "4", "5"))
        self.assertEqual(mock_input.call_count, 3)

    @patch('builtins.input', side_effect=["abc", "4", "5"])
    def test_get_sides_returns_strings(self, mock_input):
        """Даже если ввод нечисловой — метод просто возвращает строки."""
        ui = ConsoleUserInput()
        a, b, c = ui.get_sides()

        self.assertEqual(a, "abc")
        self.assertEqual(b, "4")

    @patch('builtins.input', side_effect=["", "", ""])
    def test_get_sides_with_empty_input(self, mock_input):
        """Пустой ввод не ломает метод."""
        ui = ConsoleUserInput()
        a, b, c = ui.get_sides()

        self.assertEqual((a, b, c), ("", "", ""))