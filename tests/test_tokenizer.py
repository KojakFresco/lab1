from src.calculator import Calculator, CalcError
import pytest  # type: ignore
calc = Calculator()


def test_spaces_neglecting():
    assert calc.tokenize("             1        2                   ") == [("NUM", 1.0), ("NUM", 2.0), ("EOF", None)]


def test_partitioning():
    """Токенизация бинарных операций"""
    assert calc.tokenize("1 + 2 // 4 **") == \
           [("NUM", 1.0), ("BOP", "+"), ("NUM", 2.0), ("BOP", "//"), ("NUM", 4.0), ("BOP", "**"), ("EOF", None)]
    """Унарные операции"""
    assert calc.tokenize("1 $ ~") == [("NUM", 1.0), ("UOP", "$"), ("UOP", "~"), ("EOF", None)]
    """Скобочки"""
    assert calc.tokenize("()") == [("BR", "("), ("BR", ")"), ("EOF", None)]


def test_errors():
    """Некорректный ввод и пустой ввод"""
    with pytest.raises(CalcError):
        calc.tokenize("y & u")
        calc.tokenize("      ")
