from abc import ABC, abstractmethod


class UserInput(ABC):
    """Абстрактный интерфейс для получения данных от пользователя."""

    @abstractmethod
    def get_sides(self):
        """
        Запрашивает у пользователя три стороны.
        Возвращает: (a_str, b_str, c_str)
        """
        pass


class ConsoleUserInput(UserInput):
    """Реализация через консоль (input)."""

    def get_sides(self):
        a = input("Введите сторону A: ")
        b = input("Введите сторону B: ")
        c = input("Введите сторону C: ")
        return a, b, c



#venv\Scripts\Activate.ps1