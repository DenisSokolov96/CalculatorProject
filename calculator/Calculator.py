from calculator.opn.OPNCalculation import opn, evaluate_opn, RESERVED_WORDS
from calculator.utils.CalculationUtils import expression_to_opn


class Calculator:
    """Класс, отвечающий исключительно за математику и состояние вычислений."""

    def __init__(self):
        self.history_expression = []
        self.user_expression = {}
        self.expression = ""
        self.clear()

    def set_expression(self, text: str):
        self.expression = text

    def clear(self) -> str:
        self.expression = ""
        return self.expression

    def save_variable_opn(self, name: str, value: str) -> bool:
        """Вычисляет выражение и сохраняет чистый числовой результат в переменную."""
        name = name.strip()
        value = value.strip()
        if not name or not value:
            return False
        if name in RESERVED_WORDS or name.isdigit():
            return False
        try:
            expression_for_opn = expression_to_opn(value)
            opn_res = opn(expression_for_opn, self.user_expression)
            res = str(evaluate_opn(opn_res))
            if res.endswith(".0"):
                res = res[:-2]
            if "Ошибка" not in res and "запрещено" not in res:
                self.user_expression[name] = res
                return True
        except Exception:
            pass
        return False

    def evaluate(self) -> tuple[str, str, str]:
        if not self.expression:
            return "", "", ""
        expression_for_opn = expression_to_opn(self.expression)
        try:
            opn_res = opn(expression_for_opn, self.user_expression)
            result = str(evaluate_opn(opn_res))
            if result.endswith(".0"):
                result = result[:-2]
            self.history_expression.append((self.expression, result))
            self.expression = result
            return (result,
                    f"{len(self.history_expression)}) {self.history_expression[-1][0]} = {self.history_expression[-1][1]}",
                    " ".join(opn_res))
        except ZeroDivisionError:
            self.expression = ""
            return "Ошибка: деление на 0", "", ""
        except Exception:
            self.expression = ""
            return "Неизвестная ошибка", "", ""
