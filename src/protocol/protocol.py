from src.protocol.prover import *
from src.protocol.verifier import *
from src.protocol.utils import *

ACCEPT=1
REJECT=-1
ERROR=-2


class Protocol():

    def __init__(self, T, x, s):
        self.T = T
        self.x = x
        self.s = s      #statistical security parameter
        self.N = gen_N()
        self.prover = Prover(self.N, self.T, self.x)
        self.verifier = Verifier(self.N, self.x, self.T, self.y, self.s)

    def comp(self):
        return self.prover.solve()

    def setup(self, n=4096): # n ?!
        return gen_N(n)

    def run(self):
        self.y = self.comp()
        return self.halving_protocol()

    def halving_protocol(self):
        
        """
        with big value of T it could be 
        problematic(for the memory) to use a
        recursion, therefore I'll use a normal loop
        """
      
        while not self.T == 1:
            m = self.prover.get_m()
           
            self.verifier.set_m(m)

            r = self.verifier.gen_rand()

            self.prover.set_rand(r)

            out_v= self.verifier.halve()

            out_p= self.prover.halve()

            if not out_p == out_v:
                return ERROR

        self.N, self.x, self.T, self.y = out_v

        res = self.vf()
        
        if res == ACCEPT:
            return accept()

        else:
            return reject()

        

