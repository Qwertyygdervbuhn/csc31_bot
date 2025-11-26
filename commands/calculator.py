import re

def calculate_expression(text: str):
    raw = text.strip().replace(",", ".")

    low = raw.lower()
    if low.startswith("calc "):
        expr = raw[5:].strip()
    elif low.startswith("/calc "):
        expr = raw[6:].strip()
    else:
        expr = raw

    if not re.fullmatch(r"[0-9+\-*/().\s]+", expr):
        return None

    try:
        res = eval(expr, {"__builtins__": None}, {})
    except ZeroDivisionError:
        return "Деление на ноль нельзя"
    except Exception:
        return None

    if isinstance(res, (int, float)) and float(res).is_integer():
        return str(int(res))
    return str(res)
