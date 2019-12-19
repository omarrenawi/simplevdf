from cryptography import *
from utils import *

class Prover():
    def __init__(self,N,T,x,s):
        self.N=N
        self.T=T
        self.x=x
        self.s=s
    
    
    def solve(self):
        self.y= pow(pow(x,2,N),T,N)
        return self.y

        #TODO QRN+ instead of ZN

    def get_m(self):
        
        self.m= pow(self.x,pow(2,div(self.T,2),self.N))

        return self.m



    def set_rand(self,r):

        self.r=r

    def halve(self):

        self.x= (pow(self.x,self.r,self.N) * self.m ) % self.N

        self.y= (pow(self.m,self.r,self.N) * self.y ) % self.N

        if div(self.T, 2) % 2 == 0:
            return self.N,self.x,div(self.T,2), self.y
        
        self.y=pow(self.y,2,self.N)

        self.T= div((self.T+1),2)

        return self.N, self.x,self.T,pow(self.y,2,self.N)


