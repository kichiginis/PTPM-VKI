import unittest
import sys
import os
import logging
logging.disable(logging.CRITICAL)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from delivery_service import calculate_delivery_cost


class TestDeliveryCost(unittest.TestCase):
    """Тесты для функции calculate_delivery_cost."""

    # ---------- Тесты 1-4: Валидация веса ----------

    def test_weight_below_minimum_returns_error(self):
        """Вес < 0.1 кг -> ошибка."""
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_above_maximum_returns_error(self):
        """Вес > 50 кг -> ошибка."""
        cost, date = calculate_delivery_cost(60.0, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_exactly_at_minimum_is_valid(self):
        """Вес ровно 0.1 кг -> валидно."""
        cost, date = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertNotEqual(cost, -1)

    def test_weight_exactly_at_maximum_is_valid(self):
        """Вес ровно 50 кг -> валидно."""
        cost, date = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertNotEqual(cost, -1)

    # ---------- Тесты 5-7: Валидация дистанции ----------

    def test_distance_below_minimum_returns_error(self):
        """Дистанция 0 км -> ошибка."""
        cost, _ = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_above_maximum_returns_error(self):
        """Дистанция 6000 км -> ошибка."""
        cost, _ = calculate_delivery_cost(1.0, 6000, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_boundary_5000_is_valid(self):
        """Дистанция ровно 5000 км -> валидно."""
        cost, _ = calculate_delivery_cost(1.0, 5000, "обычный")
        self.assertNotEqual(cost, -1)

    # ---------- Тесты 8-9: Валидация типа посылки ----------

    def test_invalid_package_type_returns_error(self):
        """Несуществующий тип 'мусор' -> ошибка."""
        cost, _ = calculate_delivery_cost(1.0, 100, "мусор")
        self.assertEqual(cost, -1)

    def test_all_valid_package_types_accepted(self):
        """Все три типа ('обычный', 'хрупкий', 'опасный') принимаются."""
        for ptype in ["обычный", "хрупкий", "опасный"]:
            cost, _ = calculate_delivery_cost(1.0, 100, ptype)
            self.assertNotEqual(cost, -1, f"Тип '{ptype}' должен быть валиден")

    # ---------- Тесты 10-12: Расчет стоимости ----------

    def test_base_cost_calculation(self):
        """1 кг, 100 км, обычный -> 200 + 100*5 = 700."""
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_medium_weight_applies_1_2_coefficient(self):
        """10 кг (5<w<20), 100 км -> (200+500)*1.2 = 840."""
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_heavy_weight_applies_1_5_coefficient(self):
        """25 кг (>=20), 100 км -> (200+500)*1.5 = 1050."""
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    # ---------- Тесты 13-14: Надбавки за тип ----------

    def test_fragile_package_adds_300(self):
        """Хрупкий, 1 кг, 100 км -> 700 + 300 = 1000."""
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_package_adds_1000(self):
        """Опасный, 1 кг, 100 км -> 700 + 1000 = 1700."""
        cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 1700)

    # ---------- Тесты 15-16: Экспресс (с учетом БАГА) ----------

    def test_express_doubles_cost(self): #был баг
        """
        БАГ: экспресс должен УВЕЛИЧИВАТЬ цену, но код умножает на 0.5.
        Тест зафиксирует текущее поведение (700 * 0.5 = 350).
        После исправления бага тест нужно обновить.
        """
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        # Если баг исправить на * 1.5 -> будет 1050
        # Если на * 2.0 -> будет 1400
        # Сейчас: 700 * 0.5 = 350
        self.assertEqual(cost, 1050, " Экспресс делает доставку ДЕШЕВЛЕ — это баг!")

    def test_express_does_not_affect_error_cases(self):
        """Экспресс не должен влиять на ошибочные данные."""
        cost, _ = calculate_delivery_cost(60.0, 100, "обычный", is_express=True)
        self.assertEqual(cost, -1)

    # ---------- Тесты 17-19: Расчет даты ----------

    def test_delivery_date_format_is_correct(self):
        """Дата должна быть в формате YYYY-MM-DD."""
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")

    def test_short_distance_takes_minimum_one_day(self):
        """100 км -> 1 день -> 2026-09-04."""
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_long_distance_calculates_days_correctly(self):
        """2500 км -> 2500//500 = 5 дней -> 2026-09-08."""
        _, date = calculate_delivery_cost(1.0, 2500, "обычный")
        self.assertEqual(date, "2026-09-08")

    # ---------- Тесты 20-21: Экспресс и дата ----------

    def test_express_halves_delivery_days(self):
        """ 2500 км -> 2500//500 = 5 дней -> 2026-09-08."""
        _, date = calculate_delivery_cost(1.0, 1000, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-04")

    def test_express_with_short_distance_returns_today(self): #был баг
        """

        """
        _, date = calculate_delivery_cost(1.0, 400, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-04", "/\ Экспресс доставляет за _ дней ")


if __name__ == '__main__':
    unittest.main()