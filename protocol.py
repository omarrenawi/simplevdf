import Prover, Verifier
from Prover import *
from Verifier import *

class Protocol():
    def __init__(T,x,N,s):
        self.T=T
        self.x=x
        self.N=N
        self.s=s
        init_prover()
        init_verifier()

    def init_prover():

       self.verifier=Verifier(self.N,self.x,self.T,self.y,self.s)


    def run(): 
        self.prover=Prover(self.N,self.T,self.x)
        self.y=self.prover.solve()

    def halving_protocol(N,x,T,y,prover,verifier):#TODO input?!
    
        if T == 1:
            return verifier.check()
    
        m=prover.get_m()

        #assert m in QRN+ ,reject

        r = verifier.gen_rand()

        prover.set_rand(r)

        out_v=


