from src.protocol.VDF import *

T = 2 ** 50
N = setup(512)
x = gen(N)
"""
for i in range(100):
    x = gen(N)
    assert assert_mem(x, N)
    y = gen(N)
    assert assert_mem(y, N)
    tmp = abs ((x * y) % N)
    assert assert_mem(tmp, N)
"""
y = comp(N, x, T)
pi = prov(N, x, T, y)
verify(N, x, T, y, pi)

