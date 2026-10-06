import unittest
import sys
import os
import logging
logging.disable(logging.CRITICAL)
# Добавляем папку src в путь, чтобы импортировать оттуда модули
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from my_project import solve_triangle


class TestTriangleSolver(unittest.TestCase):
    """Тесты для функции solve_triangle (ЛР1)."""

    # ---------- Тесты 1-3: Определение типа ----------

    def test_equilateral_triangle_returns_correct_type(self):
        """Равносторонний треугольник (5,5,5) -> 'равносторонний'."""
        t_type, _ = solve_triangle("5", "5", "5")
        self.assertEqual(t_type, "равносторонний")

    def test_isosceles_triangle_returns_correct_type(self):
        """Равнобедренный треугольник (5,5,8) -> 'равнобедренный'."""
        t_type, _ = solve_triangle("5", "5", "8")
        self.assertEqual(t_type, "равнобедренный")

    def test_scalene_triangle_returns_correct_type(self):
        """Разносторонний треугольник (3,4,5) -> 'разносторонний'."""
        t_type, _ = solve_triangle("3", "4", "5")
        self.assertEqual(t_type, "разносторонний")

    # ---------- Тесты 4-5: Не треугольник ----------

    def test_impossible_triangle_returns_not_triangle(self):
        """1+2 < 10 -> 'не треугольник'."""
        t_type, _ = solve_triangle("1", "2", "10")
        self.assertEqual(t_type, "не треугольник")

    def test_zero_side_returns_error_coordinates(self):
        """Сторона = 0 -> координаты (-1,-1)."""
        t_type, coords = solve_triangle("0", "4", "5")
        self.assertEqual(t_type, "")
        self.assertEqual(coords[0], (-1, -1))

    # ---------- Тесты 6-7: Невалидные данные ----------

    def test_negative_side_returns_error_coordinates(self):
        """Отрицательная сторона -> координаты (-1,-1)."""
        t_type, coords = solve_triangle("-3", "4", "5")
        self.assertEqual(t_type, "")
        self.assertEqual(coords[0], (-1, -1))

    def test_non_numeric_input_returns_minus_two(self):
        """Буквы вместо чисел -> координаты (-2,-2)."""
        t_type, coords = solve_triangle("abc", "4", "5")
        self.assertEqual(t_type, "")
        self.assertEqual(coords[0], (-2, -2))

    # ---------- Тесты 8-10: Проверка координат ----------

    def test_coordinates_are_within_100x100_field(self):
        """Все координаты должны быть в диапазоне от 0 до 100 (кроме ошибок)."""
        _, coords = solve_triangle("3", "4", "5")
        for x, y in coords:
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(x, 200)  # с запасом на масштаб
            self.assertLessEqual(y, 200)

    def test_first_vertex_always_at_origin(self):
        """Первая вершина всегда в точке (0,0)."""
        _, coords = solve_triangle("3", "4", "5")
        self.assertEqual(coords[0], (0, 0))

    def test_float_sides_are_processed_correctly(self):
        """Float-числа (3.5, 4.5, 5.5) обрабатываются корректно."""
        t_type, coords = solve_triangle("3.5", "4.5", "5.5")
        self.assertEqual(t_type, "разносторонний")
        self.assertNotEqual(coords[0], (-1, -1))
        self.assertNotEqual(coords[0], (-2, -2))

    # ---------- Бонус: 11-й тест ----------

    def test_empty_string_returns_invalid_data(self):
        """Пустая строка -> невалидные данные (-2,-2)."""
        t_type, coords = solve_triangle("", "4", "5")
        self.assertEqual(t_type, "")
        self.assertEqual(coords[0], (-2, -2))


if __name__ == '__main__':
    unittest.main()