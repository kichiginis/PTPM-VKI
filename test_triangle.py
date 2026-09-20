import unittest
from triangle_solver import solve_triangle

class TestTriangleSolver(unittest.TestCase):

    def test_equilateral(self):

        t_type, coords = solve_triangle("5", "5", "5")
        self.assertEqual(t_type, "равносторонний")

        self.assertNotEqual(coords[0], (-1, -1))

    def test_isosceles(self):

        t_type, _ = solve_triangle("5", "5", "8")
        self.assertEqual(t_type, "равнобедренный")

    def test_scalene(self):

        t_type, _ = solve_triangle("3", "4", "5")
        self.assertEqual(t_type, "разносторонний")

    def test_not_triangle(self):
        t_type, coords = solve_triangle("1", "2", "10")
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords[0], (-1, -1))

    def test_invalid_numeric(self):
        t_type, coords = solve_triangle("-3", "4", "5")
        self.assertEqual(t_type, "") # Пустая строка для нечисловых?

        self.assertEqual(coords[0], (-1, -1))

    def test_invalid_text(self):
        t_type, coords = solve_triangle("abc", "4", "5")
        self.assertEqual(t_type, "") # Пустая строка
        self.assertEqual(coords[0], (-2, -2)) # Сброс в -2

if __name__ == '__main__':
    unittest.main()