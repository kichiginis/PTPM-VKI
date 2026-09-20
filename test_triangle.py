import unittest
from triangle_solver import solve_triangle

class TestTriangleSolver(unittest.TestCase):

    def test_equilateral(self):
        # Равносторонний
        t_type, coords = solve_triangle("5", "5", "5")
        self.assertEqual(t_type, "равносторонний")
        # Проверяем, что координаты не ошибочные
        self.assertNotEqual(coords[0], (-1, -1))

    def test_isosceles(self):
        # Равнобедренный
        t_type, _ = solve_triangle("5", "5", "8")
        self.assertEqual(t_type, "равнобедренный")

    def test_scalene(self):
        # Разносторонний
        t_type, _ = solve_triangle("3", "4", "5")
        self.assertEqual(t_type, "разносторонний")

    def test_not_triangle(self):
        # Не треугольник (нарушено неравенство)
        t_type, coords = solve_triangle("1", "2", "10")
        self.assertEqual(t_type, "не треугольник")
        # Проверка сброса координат при ошибке треугольника
        self.assertEqual(coords[0], (-1, -1))

    def test_invalid_numeric(self):
        # Отрицательные числа
        t_type, coords = solve_triangle("-3", "4", "5")
        self.assertEqual(t_type, "") # Пустая строка для нечисловых?
        # В задании: "пустая строка для нечисловых данных".
        # Но для отрицательных (ошибочных числовых) - координаты (-1,-1).
        # Уточним: если данные числовые, но некорректные (отрицательные) - это ошибка.
        # В моем коде я вернул (-1,-1) для отрицательных.
        self.assertEqual(coords[0], (-1, -1))

    def test_invalid_text(self):
        # Текст вместо чисел
        t_type, coords = solve_triangle("abc", "4", "5")
        self.assertEqual(t_type, "") # Пустая строка
        self.assertEqual(coords[0], (-2, -2)) # Сброс в -2

if __name__ == '__main__':
    unittest.main()