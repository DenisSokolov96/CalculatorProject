def fact(n):
    return 1 if n <= 1 else n * fact(n - 1)


def formula_Bernoulli(n, k, p):
    '''
    :param n: Общее количество независимых испытаний (int)
    :param k: Целевое количество успешных исходов (int)
    :param p: Вероятность успеха в одном испытании (float от 0 до 1)
    :return: Вероятность ровно k успехов (float)
    '''
    q = 1 - p
    res = (fact(n) // (fact(k) * fact(n - k))) * p ** k * q ** (n - k)
    return res


def arithmetic_progression(a1, d, n, mode):
    '''
    :param a1: Первый член арифметической прогрессии (float)
    :param d: Разность арифметической прогрессии (float)
    :param n: Номер искомого члена или количество членов для суммы (int, больше 0)
    :param mode: Режим расчета: 1 - найти n-й член (a_n), 2 - найти сумму n членов (S_n) (int)
    :return: Значение n-го члена или сумма первых n членов прогрессии (float), либо -1 в качестве ошибки
    '''
    if n <= 0:
        return -1
    if mode == 1:
        return a1 + d * (n - 1)
    elif mode == 2:
        return ((2 * a1 + d * (n - 1)) // 2) * n
    else:
        return -1


def geometric_progression(b1, q, n, mode):
    '''
    :param b1: Первый член геометрической прогрессии (float)
    :param q: Знаменатель геометрической прогрессии (float, не равен 0)
    :param n: Номер искомого члена или количество членов для суммы (int, больше 0)
    :param mode: Режим расчета: 1 - найти n-й член (b_n), 2 - найти сумму n членов (S_n) (int)
    :return: Значение n-го члена или сумма первых n членов прогрессии (float), либо -1 в качестве ошибки
    '''
    if n <= 0 or q == 0:
        return -1
    if mode == 1:
        return b1 * (q ** (n - 1))
    elif mode == 2:
        if q == 1:
            return b1 * n
        return b1 * (1 - (q ** n)) // (1 - q)
    else:
        return -1

