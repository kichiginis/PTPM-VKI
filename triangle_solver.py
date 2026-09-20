import math
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def validate_input(a_str, b_str, c_str):
    """
    Проверяет входные данные.
    Возвращает: (bool, list_of_floats_or_error_code)
    """
    try:
        # Пытаемся преобразовать в float
        a = float(a_str)
        b = float(b_str)
        c = float(c_str)

        # Проверка на положительность
        if a <= 0 or b <= 0 or c <= 0:
            logging.warning("Числа должны быть положительными.")
            return False, (-1, -1)  # Ошибочные числовые данные

        return True, [a, b, c]

    except ValueError:
        # Если преобразование не удалось (нечисловые данные)
        logging.error("Введены нечисловые данные.")
        return False, (-2, -2)  # Невалидные (нечисловые) данные


def get_triangle_type(a, b, c):
    """Определяет тип треугольника."""
    # Проверка существования треугольника (неравенство треугольника)
    if a + b <= c or a + c <= b or b + c <= a:
        return "не треугольник"

    if a == b == c:
        return "равносторонний"
    elif a == b or b == c or a == c:
        return "равнобедренный"
    else:
        return "разносторонний"


def calculate_coordinates(a, b, c):
    """
    Вычисляет координаты вершин для отрисовки в поле 100x100.
    Возвращает список кортежей [(x1, y1), (x2, y2), (x3, y3)].
    """
    # Для простоты визуализации поместим одну вершину в (0,0), а вторую на ось X.
    # Но чтобы вписать в 100x100, нужно масштабировать.

    # Вершина A (начало)
    x1, y1 = 0, 0

    # Вершина B (на оси X)
    x2, y2 = a, 0

    # Вершина C (по теореме косинусов)
    # cos(gamma) = (a^2 + b^2 - c^2) / 2ab, где gamma - угол при вершине A
    try:
        cos_alpha = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
        # Ограничиваем значение из-за возможных ошибок округления float
        cos_alpha = max(-1.0, min(1.0, cos_alpha))
        sin_alpha = math.sqrt(1 - cos_alpha ** 2)

        x3 = b * cos_alpha
        y3 = b * sin_alpha
    except ZeroDivisionError:
        # На случай деления на ноль, хотя валидация должна отсечь a=0
        return [(-1, -1), (-1, -1), (-1, -1)]

    # Масштабирование под поле 100x100
    # Находим максимальную координату, чтобы вписать в квадрат
    max_coord = max(x2, x3, y3)
    if max_coord == 0: max_coord = 1  # Защита от деления на ноль

    scale = 100 / max_coord

    # Применяем масштаб и переводим в int
    coords = [
        (int(x1 * scale), int(y1 * scale)),
        (int(x2 * scale), int(y2 * scale)),
        (int(x3 * scale), int(y3 * scale))
    ]

    return coords


def solve_triangle(a_str, b_str, c_str):
    """
    Основная функция решения.
    """
    logging.info(f"Входные данные: {a_str}, {b_str}, {c_str}")

    # 1. Валидация
    is_valid, result = validate_input(a_str, b_str, c_str)

    if not is_valid:
        # Если данные невалидны, возвращаем пустую строку для типа и координаты ошибки
        return "", [result, result, result]

    a, b, c = result

    # 2. Определение типа
    tri_type = get_triangle_type(a, b, c)

    # 3. Если это не треугольник, координаты не рассчитываем (или сбрасываем)
    if tri_type == "не треугольник":
        return tri_type, [(-1, -1), (-1, -1), (-1, -1)]

    # 4. Расчет координат
    coords = calculate_coordinates(a, b, c)

    return tri_type, coords


# Блок для ручного тестирования
if __name__ == "__main__":
    # Примеры для проверки
    test_cases = [
        ("3", "4", "5"),  # Разносторонний
        ("5", "5", "5"),  # Равносторонний
        ("5", "5", "8"),  # Равнобедренный
        ("1", "2", "10"),  # Не треугольник
        ("abc", "4", "5"),  # Нечисловые данные
        ("-3", "4", "5"),  # Отрицательные числа
    ]

    for tc in test_cases:
        t_type, t_coords = solve_triangle(*tc)
        print(f"Вход: {tc} -> Тип: '{t_type}', Координаты: {t_coords}")