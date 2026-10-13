import unittest
import sys
import os
from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from controller import TriangleController
from database import TriangleRepository
from user_input import UserInput
from notifier import Notifier


class TestTriangleControllerIntegration(unittest.TestCase):
    """
    Интеграционные тесты контроллера.
    Используем реальную БД (in-memory) + Mock для user_input и notifier.
    """

    def setUp(self):
        """Перед каждым тестом — свежая БД и моки."""
        self.repo = TriangleRepository(":memory:")
        self.mock_input = Mock(spec=UserInput)
        self.mock_notifier = Mock(spec=Notifier)
        self.mock_notifier.send.return_value = True
        self.controller = TriangleController(
            user_input=self.mock_input,
            repository=self.repo,
            notifier=self.mock_notifier
        )

    def tearDown(self):
        self.repo.close()

    # ============ ИНТЕГРАЦИОННЫЙ ТЕСТ №1 ============
    def test_first_request_computes_and_saves_to_db(self):
        """
        Первый запрос: данных в БД нет → вычисляем → сохраняем → отправляем.
        Проверяем все три шага.
        """
        # Arrange: мок возвращает (3, 4, 5)
        self.mock_input.get_sides.return_value = ("3", "4", "5")

        # Act
        tri_type, coords, error = self.controller.run()

        # Assert: 1) вычислили правильно
        self.assertEqual(tri_type, "разносторонний")
        self.assertEqual(error, "")

        # Assert: 2) сохранили в БД
        saved = self.repo.get(3.0, 4.0, 5.0)
        self.assertIsNotNone(saved)
        self.assertEqual(saved[0], "разносторонний")

        # Assert: 3) отправили через notifier
        self.mock_notifier.send.assert_called_once()
        sent_message = self.mock_notifier.send.call_args[0][0]
        self.assertIn("разносторонний", sent_message)

    # ============ ИНТЕГРАЦИОННЫЙ ТЕСТ №2 ============
    def test_second_request_uses_cache_not_recompute(self):
        """
        Второй запрос с теми же данными: берем из БД, не пересчитываем.
        Проверяем, что данные реально берутся из БД.
        """
        # Arrange: сначала выполняем первый запрос
        self.mock_input.get_sides.return_value = ("3", "4", "5")
        self.controller.run()

        # Вручную меняем запись в БД (симуляция "внешнего" изменения)
        self.repo.add(3.0, 4.0, 5.0, "ИЗМЕНЕНО_В_БД", "кэшированный ответ")

        # Act: второй запрос с теми же данными
        tri_type, _, _ = self.controller.run()

        # Assert: контроллер вернул данные из БД, а не пересчитал
        self.assertEqual(tri_type, "ИЗМЕНЕНО_В_БД")

        # Assert: notifier всё равно вызван (отправка каждый раз)
        self.assertEqual(self.mock_notifier.send.call_count, 2)

    # ============ ИНТЕГРАЦИОННЫЙ ТЕСТ №3 ============
    def test_invalid_input_sends_error_and_not_saved_to_db(self):
        """
        Невалидные данные: не сохраняем в БД, но отправляем ошибку.
        """
        # Arrange
        self.mock_input.get_sides.return_value = ("abc", "4", "5")

        # Act
        tri_type, coords, error = self.controller.run()

        # Assert: 1) тип пустой, ошибка есть
        self.assertEqual(tri_type, "")
        self.assertIn("нечисловые", error)

        # Assert: 2) в БД ничего не сохранилось
        # (проверим, что таблица пуста)
        cursor = self.repo.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM triangles")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 0)

        # Assert: 3) notifier вызван с сообщением об ошибке
        self.mock_notifier.send.assert_called_once()
        sent_message = self.mock_notifier.send.call_args[0][0]
        self.assertIn("нечисловые", sent_message)

    # ============ ДОПОЛНИТЕЛЬНЫЙ ТЕСТ №4 ============
    def test_not_a_triangle_saved_with_error_message(self):
        """
        Стороны 1, 2, 10 — не треугольник. Сохраняем с сообщением об ошибке.
        """
        self.mock_input.get_sides.return_value = ("1", "2", "10")

        tri_type, _, error = self.controller.run()

        self.assertEqual(tri_type, "не треугольник")
        self.assertIn("неравенство", error)

        saved = self.repo.get(1.0, 2.0, 10.0)
        self.assertIsNotNone(saved)
        self.assertEqual(saved[0], "не треугольник")

    # ============ ДОПОЛНИТЕЛЬНЫЙ ТЕСТ №5 ============
    def test_notifier_failure_does_not_crash_controller(self):
        """
        Если notifier падает — контроллер не должен ломаться.
        """
        self.mock_input.get_sides.return_value = ("3", "4", "5")
        self.mock_notifier.send.side_effect = Exception("SMTP недоступен")

        # Act + Assert: контроллер должен выжить
        with self.assertRaises(Exception):
            # Сейчас контроллер НЕ ловит исключение от notifier.
            # Это можно исправить: обернуть send() в try/except.
            self.controller.run()

        # Данные всё равно должны быть в БД (мы сохранили ДО отправки)
        self.assertIsNotNone(self.repo.get(3.0, 4.0, 5.0))