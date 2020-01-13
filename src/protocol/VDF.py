from src.protocol.utils import *
from secrets import randbelow
import hashlib


ACCEPT=1
REJECT=-1
ERROR=-2
s = None #statistical security parameter

def setup(s):
    """
    s: statistical security parameter
    """
    return gen_N()


def gen(N, T):
    return generate_rand_residue(N)


def comp(N, x, T):
    return pow(pow(x, 2, N), T, N)

def prov(N, x, T, y):
    """
    for the fiat shamir heuristic we will use sha256
    """
    h=hashlib.sha_256()


    t=math.log(T,2)
    xn, yn= x, y
    pi=[].append(None) # fill the 0'th index
    for i in range(1,t):
        tmp = pow(xn, (pow(2, div(T, 2**i), N)), N) #assert in QRN+
        pi.append(tmp)
        tmp=(xn, div(T, 2**(i-1)),yn,pi[i])
        tmp = "".join(tmp)
        h.update(tmp.encode())
        dig=h.hexdigest()
        h=hashlib.sha_256()
        r= int(dig, 16) % s
        xn= (xn**r, pi[i], N)
        yn = (pi[i]** r, yn, N)

    return pi


def verify(N, x, T, y, pi):

    if not assert_mem(x,N):
        return REJECT

    if not assert_mem(y,N):
        return REJECT

    for i in pi:
        if not assert_mem(i, N):
            return REJECT


    xn, yn= x, y

    t = math.log(T, 2) # as input

    for i in range(1,t):
        tup = (xn, div(T, 2**i), yn, pi[i])
        tmp = "".join(tup)
        h = hashlib.sha_256()
        h.update(tmp.encode())
        hs =h.hexdigest()
        r  = int(hs, 16)
        xn = mul(xn **r, pi[i], N)
        yn = mul(pi[i]**r, yn, N)

    if yn == xn **2: #mod?
        print('ACCEPT')
        return ACCEPT
    print('REJECT')
    return REJECT