from src.calculator import Calculator, CalcError
import pytest  # type: ignore
calc = Calculator()


def test_right_expressions():
    """Проверка базовых операций и унарных знаков"""
    assert calc.calculate_rpn("10 8 - 10 ~ ~ $ **") == 1024
    assert calc.calculate_rpn("11 5 // 1.5 +") == 3.5
    assert calc.calculate_rpn("44 10 % 0.5 /") == 8

    """Проверка скобок"""
    assert calc.calculate_rpn("((10 8 -) (10 ~ ~) $ **) 2 +") == 1026

    """Ввод одиночного числа"""
    assert calc.calculate_rpn("10") == 10

def test_wrong_expressions():
    with pytest.raises(CalcError):
        """Деление на ноль"""
        calc.calculate_rpn("1 0 /")

        """Некорректная запись"""
        calc.calculate_rpn("+ 1 0 /")
        calc.calculate_rpn("1 + 2")
        calc.calculate_rpn("1 2 3 +")

        """Некорректно расставлены скобки"""
        calc.calculate_rpn("( 18 3 ) -")

        """Применение целочисленного деления к вещественным числам"""
        calc.calculate_rpn("12.2 // 3")
        calc.calculate_rpn("12.2 % 3")
