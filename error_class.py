# a = "The sky is blue"
# print(a)

# for letter in a:
#     print(letter)

def function_name():

    try:
        from my_math_calculator import sqrt
    except ModuleNotFoundError:
        from math import sqrt

    x = sqrt(4)
    print(x)


def main():
    function_name()
    from my_math_calculator import add_positive_integers
    try:
        x = add_positive_integers(-2, 3)
        print(x)
    except ValueError as err:
        print(err.__traceback__)
    # except TypeError:
    #     print("Got Type Error")
    # except:
    #     print("All other errors")


if __name__ == "__main__":
    main()
