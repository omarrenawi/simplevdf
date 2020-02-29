from src.protocol.VDF import *

T = 2 ** 10
N = setup(2048)
x = gen(N)
y = comp(N, x, T)
pi = prov(N, x, T, y)
verify(N, x, T, y, pi)

