from secrets import randbelow

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

        
    def check(self):
        
        assert T==1
        #otherwise, the halving protocol must continue
        
        return self.y == pow(self.x,2,self.N)
        #TODO Computations must be performed in QRN instead of ZN

    def halve(self):

        self.x= (pow(self.x,self.r,self.N) * self.m ) % self.N
        self.y= (pow(self.m,self.r,self.N) * self.y ) % self.N
        if div(T,2) % 2 == 0:
            return self.N,self.x,self.T //2, self.y
        
        return self.N, self.x,(self.T+1)//2 ,pow(self.y,2,self.N)


