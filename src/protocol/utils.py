import math


def div(a,b):
    return math.ceil(a/b)


# https://www.researchgate.net/publication/2273750_A_Binary_Algorithm_for_the_Jacobi_Symbol

def jacobi(x, n):
    assert x >= 0 and n > 0 and n % 2 != 0

    j = 1

    while x != 0:
        while x % 2 == 0:

            x = x // 2

            if (n % 8) == 3 or (n % 8) == 5:
                j = -j
        if x < n:
            x, n = n, x
            if (x % 4) == 3 and (n % 4) == 3:
                j = -j

        x = (x - n) // 2

        if (n % 8 == 3) or (n % 8 == 5):
            j = -j

    if n == 1:
        return j

    else:
        return 0