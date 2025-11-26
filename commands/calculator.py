import re

def calculate_expression(text: str):
    expr = text.replace(",", ".").strip()

    if not re.fullmatch(r"[0-9+\-*/().\s]+", expr):
        return None

    try:
        result = eval(expr, {"__builtins__": None}, {})
    except ZeroDivisionError:
        return "Деление на ноль нельзя"
    except Exception:
        return None

    if isinstance(result, (int, float)) and float(result).is_integer():
        return f"Результат: {int(result)}"

    return f"Результат: {result}"
