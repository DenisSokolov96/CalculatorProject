import numpy as np

from calculator.opn.OPNCalculation import opn, evaluate_opn, RESERVED_WORDS
from calculator.utils.CalculationUtils import expression_to_standard, calculate_formula_Bernoulli, \
    calculate_arithmetic_progression, calculate_geometric_progression

ENGINE_EVALUATION = {"opn": "Обратная польская нотация", "graph": "Структура граф"}


class Calculator:
    """Класс, отвечающий исключительно за математику и состояние вычислений."""

    def __init__(self):
        self.history_expression = []
        self.user_expression = {}
        self.expression = ""
        self.engine_evaluation = ENGINE_EVALUATION["opn"]
        self.clear()

    def set_expression(self, text: str):
        self.expression = text

    def set_engine(self, engine_key: str):
        if engine_key in ENGINE_EVALUATION:
            self.engine_evaluation = engine_key

    def clear(self) -> str:
        self.expression = ""
        return self.expression

    def _calculate_by_engine(self, expression_standard: str):
        match self.engine_evaluation:
            case "opn":
                opn_res = opn(expression_standard, self.user_expression)
                result = str(evaluate_opn(opn_res))
                return result, opn_res
            case "graph":
                result = "Режим графов в разработке"
                return result, ""
            case _:
                raise ValueError("Неизвестный движок вычислений")

    def save_variable(self, name: str, value: str) -> bool:
        """Вычисляет выражение и сохраняет чистый числовой результат в переменную."""
        name = name.strip()
        value = value.strip()
        if not name or not value:
            return False
        if name in RESERVED_WORDS or name.isdigit():
            return False
        try:
            expression_standard = expression_to_standard(value)
            res, engine_res = self._calculate_by_engine(expression_standard)
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
        expression_standard = expression_to_standard(self.expression)
        try:
            result = ""
            res_transform = ""
            match self.engine_evaluation:
                case "opn":
                    res_transform = opn(expression_standard, self.user_expression)
                    result = str(evaluate_opn(res_transform))
                case "graph":
                    # Заглушка для решения методом графа
                    result = "Режим графов в разработке"
                    res_transform = "Режим графов в разработке"
                case _:
                    return "Ошибка движка", "", ""
            if result.endswith(".0"):
                result = result[:-2]
            self.history_expression.append((self.expression, result))
            self.expression = result
            return (result,
                    f"{len(self.history_expression)}) {self.history_expression[-1][0]} = {self.history_expression[-1][1]}",
                    " ".join(res_transform))
        except ZeroDivisionError:
            self.expression = ""
            return "Ошибка: деление на 0", "", ""
        except Exception:
            self.expression = ""
            return "Неизвестная ошибка", "", ""

    def calculate_formula(self, formula, paramInput1, paramInput2, paramInput3, paramInput4) -> tuple[str, str] | None:
        try:
            if formula == "Формула Бернулли":
                n = int(self.user_expression.get(paramInput1, paramInput1))
                k = int(self.user_expression.get(paramInput2, paramInput2))
                p = float(self.user_expression.get(paramInput3, paramInput3.replace(',', '.')))
                err, res = calculate_formula_Bernoulli(n, k, p)
                res = str(res)
                if res.endswith(".0"):
                    res = res[:-2]
                if err == 1:
                    self.history_expression.append(res)
                    history = f"{len(self.history_expression)}) {res}"
                else:
                    history = res
                return res, history
            elif formula == "Арифметическая прогрессия":
                a1 = float(self.user_expression.get(paramInput1, paramInput1.replace(',', '.')))
                d = float(self.user_expression.get(paramInput2, paramInput2.replace(',', '.')))
                n = int(self.user_expression.get(paramInput3, paramInput3))
                mode = int(paramInput4)
                err, res = calculate_arithmetic_progression(a1, d, n, mode)
                res = str(res)
                if res.endswith(".0"):
                    res = res[:-2]
                if err == 1:
                    self.history_expression.append(res)
                    history = f"{len(self.history_expression)}) {res}"
                else:
                    history = res
                return res, history
            elif formula == "Геометрическая прогрессия":
                b1 = float(self.user_expression.get(paramInput1, paramInput1.replace(',', '.')))
                q = float(self.user_expression.get(paramInput2, paramInput2.replace(',', '.')))
                n = int(self.user_expression.get(paramInput3, paramInput3))
                mode = int(paramInput4)
                err, res = calculate_geometric_progression(b1, q, n, mode)
                res = str(res)
                if res.endswith(".0"):
                    res = res[:-2]
                if err == 1:
                    self.history_expression.append(res)
                    history = f"{len(self.history_expression)}) {res}"
                else:
                    history = res
                return res, history
        except Exception:
            return "Error", "Ошибка в вычислениях"

    def evaluate_isolated(self, expr_str: str) -> float:
        """
        Вычисляет изолированное выражение (например, точку для графика),
        НЕ изменяя историю калькулятора и его текущее состояние выражения.
        Возвращает чистый float или np.nan в случае ошибки.
        """
        if not expr_str:
            return np.nan
        try:
            expression_standard = expression_to_standard(expr_str)
            res_str, _ = self._calculate_by_engine(expression_standard)
            if "Ошибка" in res_str or "запрещено" in res_str:
                return np.nan
            return float(res_str)
        except (ZeroDivisionError, ValueError, KeyError):
            return np.nan
        except Exception:
            return np.nan

    def calculate_plot_data(self, expr: str, min_x: float, max_x: float, step: float) -> tuple[np.ndarray, np.ndarray]:
        """
        Генерирует массивы точек X и Y для построения графика.
        Автоматически адаптирует расчеты под текущий движок (ОПН или Граф).
        """
        x_array = np.arange(min_x, max_x + step, step)
        y_array = []
        match self.engine_evaluation:
            case "opn":
                for x_val in x_array:
                    x_in_degrees = np.degrees(x_val)
                    if abs(x_in_degrees) < 1e-9:
                        current_expr = expr.lower().replace('x', '0')
                    else:
                        current_expr = expr.lower().replace('x', f"({x_in_degrees})")
                    result_float = self.evaluate_isolated(current_expr)
                    y_array.append(result_float)
            case "graph":
                y_array = [0.0] * len(x_array)

            case _:
                raise ValueError("Неизвестный движок вычислений")
        y_array = np.array(y_array, dtype=float)
        y_masked = np.ma.masked_invalid(y_array)
        return x_array, y_masked
