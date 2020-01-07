from secrets import randbelow
from src.protocol.utils import *
class Verifier():
    
    def __init__(self,N,x,T,y,s):
        self.N=N
        self.x=x
        self.T=T
        self.y=y
        self.s=s #statistical security parameter


    def gen_rand(self):
        self.r= randbelow(2**self.s)

        return self.r


    def set_m(self,m): #assert m in QRN+
        self.m = m
        
    def check(self):
        assert self.T==1
        #otherwise, the halving protocol must continue
        
        return self.y == pow(self.x,2,self.N)

    def halve(self, N, x, T, y):
        x = (pow(x, self.r, N) * self.m) % N

        y = (pow(self.m, self.r, N) * y) % N

        if div(T, 2) % 2 == 0:
            return N, x, div(T, 2), y

        y = pow(y, 2, N)

        T = div((T + 1), 2)

        return N, x, T, pow(y, 2, N)