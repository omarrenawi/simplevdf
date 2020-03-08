import time
from VDF import *
from parallel_scheme import *


<<<<<<< HEAD
"""
for i in range(100):
    x = gen(N)
    assert assert_mem(x, N)
    y = gen(N)
    assert assert_mem(y, N)
    tmp = abs ((x * y) % N)
    assert assert_mem(tmp, N)
"""
def vf(pp, y_p, y, S_i, pi_i) :
    return verify(N, y_p, S_i, y, pi_i) 
    
def evaluate(N, x, T):
    res = comp(N, x, T)
    return res, prov(N, x, T, res)
    
def prov_mod(alpha):
    return alpha
    
def detailed_output(T, N, x):
    print("(simple) Solving...")
    start_time = time.time()
    y = comp(N, x, T)
    #print ("basic y=", y)
    print("... (simple) Solving done in", time.time() - start_time)
    print("(simple) Proving...")
    start_time = time.time()
    pi = prov(N, x, T, y)
    #print("basic pi=", pi)
    print("...(simple) Proving done in", time.time() - start_time)
    print("(simple) Verifying...")
    start_time = time.time()
    if (verify(N, x, T, y, pi)):
        print("... Simple output accepted in", time.time() - start_time)
    
    
    
    parallel = Parallel_scheme( T, setup, gen, evaluate, vf, prov_mod, evaluate)
    
    print("(parallel) Solving & Proving...")
    start_time = time.time()
    y_parallel, pi_parallel = parallel.eval_(N, x, T)
    print("... parallel Solving & Proving done in", time.time() - start_time)
    #print ("parallel y=", y_parallel)
    #print("parallel pi=", pi_parallel)
    print("(parallel) Verifying...")
    start_time = time.time()
    print(parallel.vf_(N, x, y_parallel, pi_parallel, T), "in", time.time() - start_time)

T = 2 ** 26
N = setup(64)
x = gen(N)
=======
T = 2 ** 10
N = setup(2048)
x = gen(N)
y = comp(N, x, T)
pi = prov(N, x, T, y)
verify(N, x, T, y, pi)
>>>>>>> 23a28786ce122d67c2d20ef16bd0f857657f04ba

detailed_output(T, N, x)