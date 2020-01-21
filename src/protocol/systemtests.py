from src.protocol.VDF import *

T = 2 ** 100
N = setup(512)
x = gen(N)

y = comp(N, x, T)

pi = prov(N, x, T, y)

assert verify(N, x, T, y, pi) == 0

