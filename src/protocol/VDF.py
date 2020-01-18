from src.protocol.utils import *

import hashlib

s = None  # statistical security parameter


def setup(s):
    """
    @input: s: statistical security parameter
    @output: N
    """
    return gen_N() ## and s?!


def gen(N):
    return generate_rand_residue(N)


def comp(N, x, T):  # solution of the RSW time-lock puzzle (but over (QR+N, ◦) not (Z∗N , ·))
    return pow(pow(x, 2, N), T, N)


def prov(N, x, T, y):

    """ for the Fiat Shamir heuristic we will use sha256
    """
    h = hashlib.sha_256()

    t = math.log(T,2)

    xn, yn = x, y

    # fill the 0'th index
    pi = [].append(None)
    for i in range(1, t):
        tmp = pow(xn, (pow(2, div(T, 2**i), N)), N)

        if not assert_mem(tmp,N):
            return reject()

        pi.append(tmp)
        tmp = (xn, div(T, 2**(i-1)), yn, pi[i])
        tmp = "".join(tmp)
        h.update(tmp.encode())
        dig = h.hexdigest()
        h = hashlib.sha_256()
        r = int(dig, 16) % (2 ** s)
        xn = mul(pow(xn, r, N), pi[i], N)
        yn = mul(pow(pi[i], r, N), yn, N)

    return pi


def verify(N, x, T, y, pi):

    if not assert_mem(x,N):
        return reject()

    if not assert_mem(y,N):
        return reject()

    for i in pi:
        if not assert_mem(i, N):
            return reject()

    xn, yn = x, y

    t = math.log(T, 2)

    for i in range(1, t):
        tup = (xn, div(T, 2**i), yn, pi[i])
        tmp = "".join(tup)
        h = hashlib.sha_256()
        h.update(tmp.encode())
        hs = h.hexdigest()
        r = int(hs, 16) % (2 ** s)
        xn = mul(pow(xn, r, N), pi[i], N)
        yn = mul(pow(pi[i], r, N), yn, N)

    if yn == xn **2:  # mod?
        return accept()

    return reject()
