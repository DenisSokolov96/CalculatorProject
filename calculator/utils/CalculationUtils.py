import math

from calculator.utils.MathUtils import formula_Bernoulli, arithmetic_progression, geometric_progression


def expression_to_standard(expression):
    if "=" in expression:
        expression = expression.replace("=", "")
    return expression


def extract_trig_func(token, i_token, expression):
    start_pos = i_token - 1
    if token == "s" and expression[start_pos:i_token + 2] == "sin":
        token = "sin"
        i_token += 2
    elif token == "c" and expression[start_pos:i_token + 2] == "cos":
        token = "cos"
        i_token += 2
    elif token == "t" and expression[start_pos:i_token + 1] == "tg":
        token = "tg"
        i_token += 1
    elif token == "c" and expression[start_pos:i_token + 2] == "ctg":
        token = "ctg"
        i_token += 2
    elif token == "a" and expression[start_pos:i_token + 5] == "arcSin":
        token = "arcSin"
        i_token = start_pos + 6
    elif token == "a" and expression[start_pos:i_token + 5] == "arcCos":
        token = "arcCos"
        i_token = start_pos + 6
    elif token == "a" and expression[start_pos:i_token + 4] == "arcTg":
        token = "arcTg"
        i_token = start_pos + 5
    elif token == "a" and expression[start_pos:i_token + 5] == "arcCtg":
        token = "arcCtg"
        i_token = start_pos + 6
    elif token == "l" and expression[start_pos:i_token + 1] == "lg":
        token = "lg"
        i_token += 1
    elif token == "l" and expression[start_pos:i_token + 1] == "ln":
        token = "ln"
        i_token += 1
    elif token == "l" and expression[start_pos:i_token + 2] == "log":
        token = "log"
        i_token += 2
    return token, i_token


def eval_trig_func(symbol, stack_res):
    a = stack_res.pop()
    if symbol == "sin":
        stack_res.append(round(math.sin(math.radians(a)), 12))
    elif symbol == "cos":
        stack_res.append(round(math.cos(math.radians(a)), 12))
    elif symbol == "tg":
        if int(a) % 180 == 90:
            return "Ошибка: tg(90) не существует!"
        stack_res.append(round(math.tan(math.radians(a)), 12))
    elif symbol == "ctg":
        if int(a) % 180 == 0:
            return "Ошибка: ctg(0) не существует!"
        stack_res.append(round(1 / math.tan(math.radians(a)), 12))
    elif symbol == "arcSin":
        if not (-1 <= a <= 1):
            return "Ошибка: аргумент arcSin должен быть от -1 до 1!"
        stack_res.append(round(math.degrees(math.asin(a)), 12))
    elif symbol == "arcCos":
        if not (-1 <= a <= 1):
            return "Ошибка: аргумент arcCos должен быть от -1 до 1!"
        stack_res.append(round(math.degrees(math.acos(a)), 12))
    elif symbol == "arcTg":
        stack_res.append(round(math.degrees(math.atan(a)), 12))
    elif symbol == "arcCtg":
        stack_res.append(round(90 - math.degrees(math.atan(a)), 12))
    elif symbol == "ln":
        if a <= 0:
            return "Ошибка: аргумент логарифма должен быть больше 0!"
        stack_res.append(round(math.log(a), 12))
    elif symbol == "lg":
        if a <= 0:
            return "Ошибка: аргумент логарифма должен быть больше 0!"
        stack_res.append(round(math.log10(a), 12))
    elif symbol == "log":
        x = stack_res.pop()
        if x <= 0 or a <= 0 or a == 1:
            return "Ошибка: недопустимые аргументы логарифма!"
        stack_res.append(math.log(x, a))
    else:
        stack_res.append(a)
        return "not found"
    return "ok"


def calculate_formula_Bernoulli(n, k, p) -> tuple[int, str]:
    if not (0 <= p <= 1):
        return 0, "Вероятность p должна быть от 0 до 1"
    if k > n:
        return 0, "k не может быть больше n"
    if n < 0 or k < 0:
        return 0, "Параметры n и k должны быть положительными"
    res = formula_Bernoulli(n, k, p)
    return 1, f"P_{n}({k}) = {res:.5f} -> {res * 100:.2f}%"


def calculate_arithmetic_progression(a1, d, n, mode) -> tuple[int, str]:
    if n <= 0:
        return 0, "Номер n должен быть больше 0"
    res = arithmetic_progression(a1, d, n, mode)
    if res != -1:
        return 1, res
    else:
        return 0, "Ошибка в параметрах"


def calculate_geometric_progression(b1, q, n, mode) -> tuple[int, str]:
    if n <= 0:
        return 0, "Номер n должен быть больше 0"
    res = geometric_progression(b1, q, n, mode)
    if res != -1:
        return 1, res
    else:
        return 0, "Ошибка в параметрах"