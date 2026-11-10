import hashlib
import requests
from bs4 import BeautifulSoup


class ForumParser:
    """Парсер цитат с сайта quotes.toscrape.com."""

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    def __init__(self, timeout=10):
        self.timeout = timeout

    def fetch_html(self, url: str) -> str:
        """Скачивает HTML по URL."""
        response = requests.get(url, headers=self.HEADERS, timeout=self.timeout)
        response.raise_for_status()  # выбросит HTTPError при 4xx/5xx
        return response.text

    def parse_html(self, html: str) -> list:
        """
        Разбирает HTML-строку и возвращает список словарей:
        [{"id": int, "name": str, "message": str}, ...]
        """
        soup = BeautifulSoup(html, "lxml")
        quotes = soup.find_all("div", class_="quote")
        result = []

        for index, quote in enumerate(quotes, start=1):
            text_el = quote.find("span", class_="text")
            author_el = quote.find("small", class_="author")

            if text_el is None or author_el is None:
                continue  # пропускаем битые блоки

            message = text_el.get_text(strip=True)
            name = author_el.get_text(strip=True)

            # Генерируем псевдо-ID из хэша текста (стабильный между запусками)
            comment_id = int(hashlib.md5(message.encode("utf-8")).hexdigest()[:8], 16)

            result.append({
                "id": comment_id,
                "name": name[:256],           # обрезаем под ограничение БД
                "message": message[:8096],
            })

        return result

    def parse_page(self, url: str) -> list:
        """Скачивает страницу и возвращает список распарсенных записей."""
        html = self.fetch_html(url)
        return self.parse_html(html)

    def save_to_db(self, parsed_data: list, repository) -> int:
        """
        Сохраняет данные в БД через DatabaseRepository.
        Возвращает количество успешно добавленных записей.
        """
        added = 0
        for item in parsed_data:
            if repository.add(item["id"], item["name"], item["message"]):
                added += 1
        return added