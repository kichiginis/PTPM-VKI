import requests
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List, Dict, Any


class ForumParser:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }

    def parse_page(self, url: str) -> List[Dict[str, Any]]:
        response = requests.get(url, headers=self.headers, timeout=15)
        response.raise_for_status()
        return self._parse_html(response.text)

    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Вспомогательный метод для парсинга из локальной HTML-фикстуры (для тестов)"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл фикстуры не найден: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return self._parse_html(html_content)

    def _parse_html(self, html_content: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html_content, 'lxml')
        posts = []

        # Находим все таблицы постов по паттерну id="post<число>"
        post_tables = soup.find_all('table', id=lambda x: x and x.startswith('post') and x[4:].isdigit())

        for table in post_tables:
            post_id = int(table['id'][4:])

            author_tag = table.find('a', class_='bigusername')
            author = author_tag.get_text(strip=True).lstrip('@') if author_tag else 'Unknown'

            message_div = table.find('div', id=lambda x: x and x.startswith('post_message_'))
            # Сохраняем внутреннюю HTML-разметку, как требуется в ТЗ
            message = message_div.decode_contents().strip() if message_div else ""

            posts.append({
                'id': post_id,
                'name': author,
                'message': message
            })

        return posts

    def save_to_db(self, parsed_data: List[Dict[str, Any]], repository: 'DatabaseRepository') -> int:
        saved_count = 0
        for item in parsed_data:
            try:
                repository.add(item['id'], item['name'], item['message'])
                saved_count += 1
            except ValueError:
                # Игнорируем дубликаты или ошибки валидации при массовом сохранении
                continue
        return saved_count