def sqrt(n):

    # We are using n itself as
    # initial approximation This
    # can definitely be improved

    if n <= 0:
        raise ValueError("sqrt cannot receive a"
                         "negative number.  You sent {}".format(n))

    x = n
    y = 1

    # e decides the accuracy level
    e = 0.000001
    while(x - y > e):
        x = (x + y)/2
        y = n / x

    return x


def add_positive_integers(a, b):
    if a < 0 or b < 0:
        raise ValueError("Cannot add negative numbers.")
    if type(a) is not int or type(b) is not int:
        raise TypeError("Cannot add non-integers")
    return a + b
