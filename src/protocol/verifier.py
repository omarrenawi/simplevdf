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
    
    
    def halve(self):

        self.x= (pow(self.x,self.r,self.N) * self.m ) % self.N

        self.y= (pow(self.m,self.r,self.N) * self.y ) % self.N

        if div(self.T, 2) % 2 == 0:
            return self.N,self.x,div(self.T,2), self.y
        
        self.y=pow(self.y,2,self.N)

        self.T= div((self.T+1),2)

        return self.N, self.x,self.T,pow(self.y,2,self.N)

    
