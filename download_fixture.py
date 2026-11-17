import requests
from pathlib import Path


def download_fixture(url: str, output_dir: str = "tests/fixtures", filename: str = "fixture_cyberforum.html"):
    target_path = Path(output_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    full_file_path = target_path / filename

    # Максимально реалистичные заголовки современного браузера
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }

    print(f"Начинаем скачивание: {url}")

    try:
        # Используем сессию для поддержания "поведения" браузера
        with requests.Session() as session:
            response = session.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            with open(full_file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)

            file_size = full_file_path.stat().st_size
            print(f"Успешно! Файл сохранен: {full_file_path.resolve()}")
            print(f"Размер файла: {file_size} байт.")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
        print("\nСАЙТ ЗАБЛОКИРОВАЛ АВТОМАТИЧЕСКОЕ СКАЧИВАНИЕ.")
        print("Используйте Вариант 2 (ручное сохранение) ниже")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    TARGET_URL = "https://www.cyberforum.ru/development/thread2771076.html"
    download_fixture(TARGET_URL)