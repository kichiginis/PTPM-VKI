import math


class TriangleSolver:
    """Класс вычислений вида треугольника и координат его вершин."""

    @staticmethod
    def solve(a_str, b_str, c_str):
        """
        Основной метод (из ЛР1).
        Возвращает: (тип_треугольника, [координаты], сообщение_об_ошибке)
        """
        try:
            a = float(a_str)
            b = float(b_str)
            c = float(c_str)
        except (ValueError, TypeError):
            return "", [(-2, -2)] * 3, "Введены нечисловые данные"

        if a <= 0 or b <= 0 or c <= 0:
            return "", [(-1, -1)] * 3, "Числа должны быть положительными"

        # Неравенство треугольника
        if a + b <= c or a + c <= b or b + c <= a:
            return "не треугольник", [(-1, -1)] * 3, "Нарушено неравенство треугольника"

        # Определение типа
        if a == b == c:
            tri_type = "равносторонний"
        elif a == b or b == c or a == c:
            tri_type = "равнобедренный"
        else:
            tri_type = "разносторонний"

        # Координаты
        x1, y1 = 0, 0
        x2, y2 = a, 0

        cos_alpha = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
        cos_alpha = max(-1.0, min(1.0, cos_alpha))
        sin_alpha = math.sqrt(1 - cos_alpha ** 2)

        x3 = b * cos_alpha
        y3 = b * sin_alpha

        max_coord = max(x2, x3, y3) or 1
        scale = 100 / max_coord

        coords = [
            (int(x1 * scale), int(y1 * scale)),
            (int(x2 * scale), int(y2 * scale)),
            (int(x3 * scale), int(y3 * scale)),
        ]
        return tri_type, coords, ""