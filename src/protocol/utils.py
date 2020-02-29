import math
import gensafeprime
from secrets import randbelow



def jacobi(x, n):
    """

     https://www.researchgate.net/publication/2273750_A_Binary_Algorithm_for_the_Jacobi_Symbol
    :return: jacobi symbol of x in n
    """

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


def gen_N(b=4096):
    """

    :param b: size of N in bits
    :return: b bits Modulus N
    """
    p = gensafeprime.generate(b // 2)
    q = gensafeprime.generate(b // 2)
    return p * q


def mul(a, b, N):
    """

    :return: a * b in QRN+
    """
    return abs(((a % N) * (b % N)) % N)


def div(a, b):
    """

    :return:⎡ a / b ⎤
    """
    return math.ceil(a / b)


# represent x as {−(N − 1)/2, . . . , (N − 1)/2}
def enc(x, N):
    assert -1 < x <= N
    return x - (N - 1) / 2



def assert_mem(a, N):
    """

    :return: True iff a is quadratic residue in QRN+
    """
    #a = enc(a, N) #TODO!!
    return a >= 0 and jacobi(a, N) == 1


def generate_rand_residue(N):
    """
    Generate a random quadratic residue x
    """

    tmp = randbelow(N)
    while not assert_mem(tmp, N):
        tmp = randbelow(N)

    return tmp


def reject():
    print("REJECTED!")
    return -1


def accept():
    print("ACCEPTED")
    return 0


def error():
    print("ERROR")
    return -2
