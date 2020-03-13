import time
import argparse
import os
import sys
from tabulate import tabulate

from VDF import *
from parallel_scheme import *

def vf(pp, y_p, y, S_i, pi_i) :
    return verify(N, y_p, S_i, y, pi_i) 
    
def evaluate(N, x, T):
    res = comp(N, x, T)
    return res, prov(N, x, T, res)
    
def prov_mod(alpha):
    return alpha
    
def simple_VDF(T, N, x):
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
    
def tight_VDF(T, N, x): 
    parallel = Parallel_scheme( T, setup, gen, evaluate, vf, prov, comp)
    print("(parallel) Solving & Proving...")
    start_time = time.time()
    y_parallel, pi_parallel = parallel.eval_(N, x, T)
    print("... parallel Solving & Proving done in", time.time() - start_time)
    #print ("parallel y=", y_parallel)
    #print("parallel pi=", pi_parallel)
    print("(parallel) Verifying...")
    start_time = time.time()
    print(parallel.vf_(N, x, y_parallel, pi_parallel, T), "in", time.time() - start_time)

def complete(t, N, x):
    print("Computing both VDF schemes on input 2^", t, "=", 2**t)
    simple_VDF(2 ** t, N, x)
    tight_VDF(2 ** t, N, x)
    
def simple(t, N, x):
    print("Computing simple VDF scheme on input 2^", t, "=", 2**t)
    simple_VDF(2 ** t, N, x)
    
def tight(t, N, x):
    print("Computing tight VDF scheme on input 2^", t, "=", 2**t)
    tight_VDF(2 ** t, N, x)

def table(t1, t2, N, x):
    metrics = ["t", "simple evaluate", "tight evaluate", "simple verify", "tight verify"]
    values = list()
    for i in range (t1, t2 + 1):
        T = 2 ** i
        row = [i]
        start_time = time.time()
        y = comp(N, x, T)
        pi = prov(N, x, T, y)
        row.append(time.time() - start_time)
        parallel = Parallel_scheme( T, setup, gen, evaluate, vf, prov, comp)
        start_time = time.time()
        y_parallel, pi_parallel = parallel.eval_(N, x, T)
        row.append(time.time() - start_time)
        start_time = time.time()
        if (verify(N, x, T, y, pi)):
            row.append(time.time() - start_time)
        else:
            print("Simple verification failed")
            sys.exit()

        start_time = time.time()
        if (parallel.vf_(N, x, y_parallel, pi_parallel, T) == "Parallel output accepted"):
            row.append(time.time() - start_time)
        else:
            print("Parallel verification failed")
            sys.exit()
        values.append(row)
    print(tabulate(values, headers = metrics, tablefmt="grid"))
    
if __name__ == "__main__":
    t = 15          # default value
    t_start = 15
    t_end = 27
    N = setup(64)
    x = gen(N)
    max_t = 1000
    
    # argparse section
    vdf_parser = argparse.ArgumentParser(description='Simple and tight VDF implementation')
    vdf_parser.add_argument('t_parameter', metavar='t', type=int, help='Timing parameter t -> using T=2^t')
    vdf_parser.add_argument('-s', '--simple', action='store_true', help="just compute simple VDF")
    vdf_parser.add_argument('-t', '--tight', action='store_true', help="just compute tight (parallel) VDF")
    vdf_parser.add_argument('-c', '--compare', action='store_true', help="compares running time of both schemes with different inputs")
    args = vdf_parser.parse_args()
    input_t = args.t_parameter
    if args.compare:
        table(t_start, t_end, N, x);
        sys.exit()
    if (input_t > 1 and input_t < max_t):
        t = int(input_t)
    else :
        print("given t out of range ( 1 -", max_t, ") hence using default t =", t)
    if args.simple:
        simple(t, N, x)
    if args.tight:
        tight(t, N, x)
    if not(args.simple or args.tight):
        complete(t, N, x)
    
    