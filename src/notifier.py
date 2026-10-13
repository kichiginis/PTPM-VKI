from abc import ABC, abstractmethod


class Notifier(ABC):
    """Абстрактный интерфейс для отправки результата."""

    @abstractmethod
    def send(self, message: str) -> bool:
        """Отправляет сообщение. Возвращает True, если успешно."""
        pass


class EmailNotifier(Notifier):
    """
    Имитация отправки на email-сервер.
    В реальном проекте здесь был бы smtplib.
    """

    def send(self, message: str) -> bool:
        # Имитация: "отправляем" и пишем в консоль
        print(f"[EMAIL] Отправлено сообщение: {message}")
        return True