from src.protocol.utils import *

import hashlib

s = 2  # statistical security parameter


def setup(s):
    """

    input: s: statistical security parameter
    output: N
    """
    return gen_N(2 * s)  # can be change


def gen(N):
    """

    :param N: Modulus N
    :return: x in QR+_{N}
    """
    return generate_rand_residue(N)


def comp(N, x, T):
    """
     solution of the RSW time-lock puzzle (but over (QR+_{N}, ◦) not (Z∗_{N}, ·))
    :param N: Modulus
    :param x: random integer in QRN+_{N}
    :param T: an integer such that T = 2 ** t for some natural number t
    :return: x**(2**T) in QR+_{N}
    """

    print("Solving ...")
    res = pow(x, 2 ** T, N)
    res= abs(res)
    print("done")
    return res


def prov(N, x, T, y):
    """

    :return: a proof that y = x ** (2 **T) in QRN+
    """

    if T < 0 or N < 0:
        return error()

    if not assert_mem(x, N):
        print("{} is not member in {}".format(x, N))
        return error()

    if not assert_mem(y, N):
        print("{} is not member in {}".format(y, N))
        print("y= %d, N=%d " %(y, N))
        return error()


    print("Proving ...")

    # for the Fiat Shamir heuristic we will use sha256

    h = hashlib.sha256()

    t = int(math.log(T, 2))

    if not 2 ** int(t) == T:
        print("T must be equal 2 ** t ")
        return error()

    xn, yn = x, y

    pi=[]

    for i in range(t):

        tmp = abs (pow(xn, 2 ** (T // (2 ** (i+1) )), N))
        pi.append(tmp)
        tmp = "{}{}{}{}".format(xn, T // 2 ** i, yn, pi[i])
        h.update(tmp.encode())
        dig = h.hexdigest()
        h = hashlib.sha256()
        r = int(dig, 16)# % (2 ** s)
        xn = mul(pow(xn, r, N), pi[i], N)
        yn = mul(pow(pi[i], r, N), yn, N)

    print("done")

    return pi


def verify(N, x, T, y, pi):
    """

    :param y: The solution (x ** (2 ** T) in QRN+)
    :param pi: The proof
    :return: True iff y has been computed correctly
    """

    if T < 0 or N < 0:
        print("T and N may not be negative")
        return reject()

    if not isinstance(pi, list):
        print("proof must be a list")
        return reject()

    if len(pi) == 0:
        print("poof may not be empty!")
        return reject()

    print("Verifying ... ")

    if not assert_mem(x, N):
        print("{} is not member in {}".format(x, N))
        return reject()

    if not assert_mem(y, N):
        print("{} is not member in {}".format(y, N))
        print("y= %d, N=%d " %(y, N))
        return reject()

    for i in pi:
        if not assert_mem(i, N):
            print("i = {} is not a member in {}".format(i, N))
            return reject()

    xn, yn = x, y

    t = int(math.log(T, 2))

    for i in range(t):
        tmp = "{}{}{}{}".format(xn, T // 2 ** i, yn, pi[i])
        h = hashlib.sha256()
        h.update(tmp.encode())
        hs = h.hexdigest()
        r = int(hs, 16) # % (2 ** s)
        xn = mul(pow(xn, r, N), pi[i], N)
        yn = mul(pow(pi[i], r, N), yn, N)

    if yn  == xn ** 2 % N:
        return accept()

    print("Verification failed!\n{} != {}".format(yn, xn ** 2 % N))
    return reject()
