from utils import *

class Prover():
    def __init__(self, N, T, x, s):
        self.N=N
        self.T=T
        self.x=x
        self.s=s #statistical security parameter

    def solve(self):
        self.y= pow(self.x, 2 ** self.T, self.N)
        return self.y

    def get_m(self):
        
        self.m= pow(self.x,pow(2,div(self.T,2),self.N))
        return self.m

    def set_rand(self,r):
        self.r =r

    def halve(self, N, x, T, y):

        x = (pow(x, self.r, N) * self.m) % N

        y = (pow(self.m, self.r, N) * y) % N

        if div(T, 2) % 2 == 0:
            return N, x, div(T, 2), y
        
        y = pow(y, 2, N)

        T = div((T+1),2)

        return N, x, T, pow(y, 2, N)


