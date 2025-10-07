from src.calculator import Calculator


def main() -> None:
    # result = Calculator.calculate_rpn(input())
    # print(result)
    calc = Calculator()
    print("Калькулятор. для выхода напишите Стоп")
    while True:
        expr = input("Введите выражение в обратной польской нотации:\n")
        if expr == "Стоп":
            break
        else:
            print(calc.calculate_rpn(expr))


if __name__ == "__main__":
    main()
