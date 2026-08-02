from collections import deque

from calculator.utils.CalculationUtils import extract_trig_func, eval_trig_func
from calculator.utils.MathUtils import fact

PRIORITY = {
    "(": 0, ")": 0, ",": 0,
    "+": 1, "-": 1,
    "*": 2, "/": 2,
    "^": 3, "**": 3, "!": 3, "√": 3,
    "sin": 4, "cos": 4, "tg": 4, "ctg": 4, "arcSin": 4, "arcCos": 4, "arcTg": 4, "arcCtg": 4, "log": 4, "ln": 4,
    "lg": 4
}
CONST = {
    "e": "2.71828182846", "g": "9.80665",
    "π": "3.14159265359", "p": "3.14159265359",
    "φ": "1.61803", "f": "1.61803"
}
RESERVED_WORDS = set(PRIORITY.keys()) | set(CONST.keys())

def opn(expression, user_expression):
    if user_expression is None:
        user_expression = {}
    expression = expression.replace(" ", "")
    stack = deque()
    res = []
    i_token = 0
    while i_token < len(expression):
        token = expression[i_token]
        i_token += 1
        token, i_token = extract_trig_func(token, i_token, expression)

        if token.isalpha() and token not in PRIORITY and token not in CONST:
            while i_token < len(expression) and expression[i_token].isalnum():
                token += expression[i_token]
                i_token += 1

        if token in user_expression:
            res.append(str(user_expression[token]))
        elif token in CONST:
            res.append(CONST[token])
        elif token.isdigit() or token == ".":
            while i_token < len(expression) and (expression[i_token].isdigit() or expression[i_token] == "."):
                token += expression[i_token]
                i_token += 1
            res.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                res.append(stack.pop())
            if stack and stack[-1] == "(":
                stack.pop()
            if stack and stack[-1] in PRIORITY and PRIORITY[stack[-1]] == 4:
                res.append(stack.pop())
        elif token == ",":
            while stack and stack[-1] != "(":
                res.append(stack.pop())
        elif token in PRIORITY:
            if i_token < len(expression) and token == "*" and expression[i_token] == "*":
                token = "^"
                i_token += 1
            if token == "-":
                i_prev = i_token - 2
                if i_prev < 0 or expression[i_prev] in PRIORITY or expression[i_prev] == "(":
                    res.append("0")
            if token in ("^", "**"):
                while stack and PRIORITY[token] < PRIORITY[stack[-1]]:
                    res.append(stack.pop())
            else:
                while stack and PRIORITY[token] <= PRIORITY[stack[-1]]:
                    res.append(stack.pop())
            stack.append(token)
        else:
            return ["Error", token]
    while stack:
        operator = stack.pop()
        if operator not in "()":
            res.append(operator)
    return res


def evaluate_opn(res):
    if len(res) == 2 and res[0] == "Error":
        return f"Неизвестный символ: {res[1]}"
    stack_res = deque()
    for symbol in res:
        if symbol[-1].isdigit():
            stack_res.append(float(symbol))
            continue
        eval_trig_func_res = eval_trig_func(symbol, stack_res)
        if eval_trig_func_res == "ok":
            continue
        elif eval_trig_func_res != "not found":
            return eval_trig_func_res
        a = stack_res.pop()
        if symbol == "+":
            stack_res.append(stack_res.pop() + a)
        elif symbol == "-":
            stack_res.append(stack_res.pop() - a)
        elif symbol == "*":
            stack_res.append(stack_res.pop() * a)
        elif symbol == "/":
            if a != 0:
                stack_res.append(stack_res.pop() / a)
            else:
                return "Деление на 0, запрещено!"
        elif symbol in ["^", "**"]:
            stack_res.append(stack_res.pop() ** a)
        elif symbol == "√":
            stack_res.append(a ** (1 / 2))
        elif symbol == "!":
            stack_res.append(float(fact(int(a))))
    return stack_res.pop()
