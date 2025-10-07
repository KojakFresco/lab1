import operator
import re


class CalcError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def do_bin_operation(num1: float, num2: float, op: str) -> float:
    """ Вычислить значение бинарной операции """
    if op == "//" or op == "%":
        if num1 % 1 != 0 or num2 % 1 != 0:
            raise CalcError(f'Операция "{op}" применима только к целым числам')
        num1, num2 = int(num1), int(num2)
        if op == "//":
            return float(num1 // num2)
        else:
            return float(num1 % num2)
    else:
        operations = {'+': operator.add, '-': operator.sub,
                      "*": operator.mul, "/": operator.truediv, "**": operator.pow}
        if op == "/" and num2 == 0:
            raise CalcError("Деление на ноль не определено")
        return operations[op](num1, num2)


class Calculator:
    def __init__(self):
        self.TOKEN_RE = re.compile(r"""
                    \s*
                    (
                        \d+(?:\.\d+)?         # число
                      | \*\* | //             # двойные токены
                      | [%()+\-*/$~]           # одиночные токены
                    )
                """, re.VERBOSE)

    def calculate_rpn(self, expr: str) -> float:
        """ Вычислить значение выражения в обратной польской записи """
        tokens = self.tokenize(expr)
        if tokens[0][0] == "BOP" or tokens[0][0] == "UOP":
            raise CalcError(f'Некорректная запись: выражение не должно начинаться с "{tokens[0][1]}"')

        stack: list = []

        for data in tokens:
            match data[0]:
                case "NUM":
                    stack.append(float(data[1]))
                case "BOP":
                    if len(stack) < 2:
                        raise CalcError("Неверное выражение")
                    num2, num1 = stack.pop(), stack.pop()
                    payload = do_bin_operation(num1, num2, data[1])
                    stack.append(payload)
                case "UOP":
                    num = stack.pop()
                    if data[1] == "~":
                        stack.append(-num)
                    else:
                        stack.append(num)
                case "BR":
                    if data[1] == "(":
                        stack.append("(")
                    else:
                        el2, el1 = stack.pop(), stack.pop()
                        if el1 == "(" and type(el2) is float:
                            stack.append(el2)
                        else:
                            raise CalcError("Неверное расположение скобок")

                    pass
                case "EOF":
                    if len(stack) == 1:
                        pass
                    else:
                        raise CalcError("Неверное выражение")
        return stack[0]

    def tokenize(self, src: str) -> list:
        """ Разбить строку на токены: числа, операторы и скобки
        Для числа кладём ("NUM", float_value).
        Для бинарного оператора кладём ("BOP", символ).
        Для унарного оператора кладём ("UOP", символ).
        Для скобок кладём ("BR", скобка).
        В конец добавляем ("EOF", None). """
        if not src or not src.strip():
            raise CalcError("Пустой ввод")

        pos = 0
        out: list[tuple[str, float | str | None]] = []

        while pos < len(src):
            m = self.TOKEN_RE.match(src, pos)
            if not m and not(re.match(r"^\s*$", src[pos:])):
                raise CalcError(f"Некорректный ввод около: '{src[pos:]}'")

            if not m:
                out.append(("EOF", None))
                return out

            t = m.group(1)
            pos = m.end()

            if t[0].isdigit():
                out.append(("NUM", float(t)))
            elif t in "**//%+-":
                out.append(("BOP", t))
            elif t in "~$":
                out.append(("UOP", t))
            else:
                out.append(("BR", t))

        out.append(("EOF", None))
        return out
