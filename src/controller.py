import logging
from triangle_solver import TriangleSolver
from database import TriangleRepository
from user_input import UserInput
from notifier import Notifier


class TriangleController:
    """
    Контроллер, реализующий бизнес-логику сквозного сценария:
    1. Получить данные от пользователя.
    2. Проверить наличие записи в БД.
    3. Если нет — вычислить, сохранить в БД.
    4. Отправить результат через Notifier.
    5. Вернуть результат.
    """

    def __init__(self, user_input: UserInput, repository: TriangleRepository, notifier: Notifier):
        # Dependency Injection: все зависимости передаются извне
        self.user_input = user_input
        self.repository = repository
        self.notifier = notifier

    def run(self):
        """
        Основной сценарий.
        Возвращает: (тип_треугольника, координаты, сообщение_об_ошибке)
        """
        # Шаг 1. Получить данные от пользователя
        a_str, b_str, c_str = self.user_input.get_sides()
        logging.info(f"Контроллер получил данные: {a_str}, {b_str}, {c_str}")

        # Нормализация для БД (числа должны быть float)
        try:
            a = float(a_str)
            b = float(b_str)
            c = float(c_str)
        except (ValueError, TypeError):
            logging.warning("Нечисловые данные — в БД не сохраняем")
            tri_type, coords, error = TriangleSolver.solve(a_str, b_str, c_str)
            message = f"Тип: {tri_type or 'неизвестно'}, Ошибка: {error}"
            self.notifier.send(message)
            return tri_type, coords, error

        # Шаг 2. Проверка БД
        cached = self.repository.get(a, b, c)

        if cached is not None:
            # Есть запись — берем из БД
            logging.info("Запись найдена в БД — используем кэш")
            tri_type, error = cached
            # Координаты пересчитаем (в БД не храним)
            _, coords, _ = TriangleSolver.solve(a_str, b_str, c_str)
        else:
            # Нет записи — вычисляем и сохраняем
            logging.info("Записи в БД нет — вычисляем заново")
            tri_type, coords, error = TriangleSolver.solve(a_str, b_str, c_str)
            self.repository.add(a, b, c, tri_type, error)

        # Шаг 3. Отправка результата
        message = f"Результат для сторон ({a}, {b}, {c}): тип='{tri_type}', ошибка='{error}'"
        self.notifier.send(message)

        # Шаг 4. Возврат результата
        return tri_type, coords, error
