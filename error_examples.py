# First Example

a = "The sky is blue"
print(a)

for letter in a:
    print(letxter)


# Second Example
def calc_square_root(n):

    from my_calculator import sqrt

    answer = sqrt(n)
    return answer


def main():
    print(calc_square_root(2))


if __name__ == "__main__":
    main()


# Third Example
def calc_square_root(n):

    try:
        from my_calculator import sqrt
    except ModuleNotFoundError:
        print("This module is not found, use builtins instead")
        from math import sqrt

    answer = sqrt(n)
    return answer


def main():
    print(calc_square_root(2))


if __name__ == "__main__":
    main()


# Raise Example
def test_sqrt_error():
    import pytest
    from calculator import sqrt
    with pytest.raises(ValueError):
        answer = sqrt(-2)


# Fibonacci
def fibonacci(fib_list):
    next_number = fib_list[-2] + fib_list[-1]
    fib_list.append(next_number)
    if next_number < 100:
        fibonacci(fib_list)
    return fib_list


def main():
    fib_list = [0, 1]
    fib_list = fibonacci(fib_list)
    print(fib_list)


if __name__ == '__main__':
    main()
