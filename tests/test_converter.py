import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from converter import Converter


class TestConverterDo(unittest.TestCase):
    """Тесты для метода Converter.do."""


    def test_zero_raises_value_error(self):
        """x == 0.0 -> ValueError."""
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    def test_zero_raises_with_message(self):
        """Сообщение исключения должно содержать информацию об ошибке."""
        with self.assertRaises(ValueError) as ctx:
            Converter.do(0.0)
        self.assertIn("нул", str(ctx.exception).lower())


    def test_x_equals_upper_boundary_100_7_returns_1000(self):
        """x = 100.7 (граница включена) -> 1000."""
        self.assertEqual(Converter.do(100.7), 1000)

    def test_x_just_above_upper_boundary_returns_1000(self):
        """x = 100.8 -> 1000."""
        self.assertEqual(Converter.do(100.8), 1000)

    def test_x_much_above_upper_boundary_returns_1000(self):
        """x = 1000.0 -> 1000."""
        self.assertEqual(Converter.do(1000.0), 1000)


    def test_x_just_below_upper_boundary_returns_int(self):
        """x = 100.6 -> int(100.6) = 100."""
        self.assertEqual(Converter.do(100.6), 100)

    def test_positive_fractional_returns_int(self):
        """x = 65.7 -> 65."""
        self.assertEqual(Converter.do(65.7), 65)

    def test_positive_less_than_one_returns_zero(self):
        """x = 0.1 -> int(0.1) = 0."""
        self.assertEqual(Converter.do(0.1), 0)


    def test_x_equals_lower_boundary_minus_30_4(self):
        """x = -30.4 (граница включена) -> int(-30.4) - 5 = -30 - 5 = -35."""
        self.assertEqual(Converter.do(-30.4), -35)

    def test_x_just_above_lower_boundary_minus_30_3(self):
        """x = -30.3 -> int(-30.3) - 5 = -30 - 5 = -35."""
        self.assertEqual(Converter.do(-30.3), -35)

    def test_negative_fractional_returns_int_minus_5(self):
        """x = -15.5 -> int(-15.5) - 5 = -15 - 5 = -20."""
        self.assertEqual(Converter.do(-15.5), -20)

    def test_negative_less_than_one_returns_minus_5(self):
        """x = -0.1 -> int(-0.1) - 5 = 0 - 5 = -5."""
        self.assertEqual(Converter.do(-0.1), -5)


    def test_x_equals_lower_boundary_minus_30_5(self):
        """x = -30.5 (граница включена) -> -2000."""
        self.assertEqual(Converter.do(-30.5), -2000)

    def test_x_just_below_lower_boundary_minus_30_6(self):
        """x = -30.6 -> -2000."""
        self.assertEqual(Converter.do(-30.6), -2000)

    def test_x_much_below_lower_boundary(self):
        """x = -1000.0 -> -2000."""
        self.assertEqual(Converter.do(-1000.0), -2000)


    def test_returns_int_for_positive(self):
        """Для положительного числа возвращается int."""
        result = Converter.do(65.7)
        self.assertIsInstance(result, int)

    def test_returns_int_for_negative(self):
        """Для отрицательного числа возвращается int."""
        result = Converter.do(-15.5)
        self.assertIsInstance(result, int)


if __name__ == '__main__':
    unittest.main()