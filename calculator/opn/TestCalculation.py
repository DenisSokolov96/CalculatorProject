import unittest

from calculator.opn.OPNCalculation import opn, evaluate_opn


class CalculationTestCase(unittest.TestCase):
    def test_1(self):
        input_str = "2 * 3 ^ 4 + 5"
        result = opn(input_str)
        self.assertEqual(evaluate_opn(result), 167)

    def test_2(self):
        input_str = "(1+6)*2-3"
        result = opn(input_str)
        self.assertEqual(evaluate_opn(result), 11)

    def test_3(self):
        input_str = "(5+(5-8)*3)/5"
        result = opn(input_str)
        self.assertEqual(evaluate_opn(result), -0.8)

    def test_4(self):
        input_str = "20+2**5"
        result = opn(input_str)
        self.assertEqual(evaluate_opn(result), 52)

    def test_5(self):
        input_str = "2 ^ 3 ^ 2"
        result = opn(input_str)
        self.assertEqual(evaluate_opn(result), 512)

    def test_6(self):
        input_str = "2*(5+(1+(7-9)*(5-7)))"
        result = opn(input_str)
        self.assertEqual(evaluate_opn(result), 20)

    def test_7(self):
        input_str = "5/0"
        result = opn(input_str)
        self.assertEqual(evaluate_opn(result), "Деление на 0, запрещено!")

    def test_8(self):
        input_str = "5+h"
        result = opn(input_str)
        evaluate = evaluate_opn(result)
        self.assertEqual(evaluate, f"Неизвестный символ: {result[1]}")

    def test_9(self):
        input_str = "5"
        result = opn(input_str)
        self.assertEqual(evaluate_opn(result), 5)

    def test_10(self):
        input_str = "-3+5"
        result = opn(input_str)
        self.assertEqual(evaluate_opn(result), 2)

    def test_11(self):
        input_str = "-5.5*2,6"
        result = opn(input_str)
        self.assertEqual(evaluate_opn(result), -14.3)

    def test_12(self):
        input_str = "(1+6)!*2-3"
        result = opn(input_str)
        self.assertEqual(evaluate_opn(result), 10077)

    def test_13(self):
        input_str = "√25"
        result = opn(input_str)
        self.assertEqual(evaluate_opn(result), 5)

    def test_14(self):
        input_str = "e/e"
        result = opn(input_str)
        self.assertEqual(evaluate_opn(result), 1)


if __name__ == '__main__':
    unittest.main()
