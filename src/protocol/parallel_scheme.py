from .VDF import *
from multiprocessing import Process, Queue 


class Parallel_scheme():
	# weakly efficient and self-composable VDF
	def __init__(self, T, setup, gen, evaluate, vf, prove, comp):
		self.T = T
		self.setup = setup
		self.gen = gen 
		self.evaluate = evaluate
		self.vf = vf
		self.prove = prove
		self.comp = comp
		
		# multiprocessing queue to add π
		self.q_eval = Queue()
		self.q_vf = Queue()
		self.L_init = list()
		
<<<<<<< HEAD
	def psi(self, x):
		return x
			
	def par_prove(self, N, x, T, y):
		self.q_eval.put(self.prove(N, x, T, y))
	
	def par_prove_alpha(self, alpha):
		self.q_eval.put(self.prove(alpha))
	
	def par_vf(self, pp, y_i_1, y_i, S_i, pi_i):
		self.q_vf.put(self.vf(pp, y_i_1, y_i, S_i, pi_i)) 
	
		
=======
	def par_prove(self, a, q):
		q.put(self.prove(a))
	
	def par_vf(self, pp, y_i_1, y_i, S_i, q):
		q.put(self.vf(pp, y_i_1, y_i, S_i))

>>>>>>> 23a28786ce122d67c2d20ef16bd0f857657f04ba
	def setup_(self, lambd):
		return self.setup(lambd)
	
	def gen_(self, pp):
		return self.gen(pp)
	
<<<<<<< HEAD
	def eval_(self, pp, x, T):
		# for psi(S) = S
		S = math.ceil(T / 2)
=======
	def eval_(self, pp, x, T, S = 0, fst = True):
		# multiprocessing queue to add π
		q= Queue()

		if fst:
			while (True):
				if (S + self.psi(S) >= T): break

				else: S += 1

>>>>>>> 23a28786ce122d67c2d20ef16bd0f857657f04ba
		if (S <= 1):
			y, alpha = self.comp(pp, x, T)
			return (y, self.L_init)
		else:
			y, alpha = self.comp(pp, x, S)
			#alpha = self.prove(pp, x, T, y)	# not sure with this (why computed at all?)
			process_pi = Process(target=self.par_prove_alpha, args=(alpha,))
			#process_pi = Process(target=self.par_prove, args=(pp, x, T, y))
			process_pi.start()
			y_ , L = self.eval_(pp, y, T - S)
			process_pi.join()
			pi = self.q_eval.get()
			L.insert(0, (y, pi))
			return (y_, L)
			
<<<<<<< HEAD
	def vf_(self, pp, x, y_in, pi_in, T):
=======
	def vf_(self, pp, x, y_in, pi, T):
>>>>>>> 23a28786ce122d67c2d20ef16bd0f857657f04ba
		# multiprocessing queue to add b_i
		n = 0
		y = []
<<<<<<< HEAD
		pi = []	
		y.append(x);
		pi.append(x); # dummy, π[0] should be ? empty ? 
		for el in pi_in:		# parse pi into list of n y[i],pi[i] tupels
			fst, snd = el
			y.append(fst)
			pi.append(snd)
			n += 1
		S_lst = [None] 
		s_sum = 0
=======
		y.add(x); # TODO: replace add with append except if it should be a set then change the type of y
		pi = []	
		for fst, snd in pi:			# parse pi into list of n y[i],pi[i] tupels
			y.add(fst)
			pi.add(snd)

		S_lst = []
		b_lst = []
>>>>>>> 23a28786ce122d67c2d20ef16bd0f857657f04ba
		S_lst[0] = T
		process_b = [None] * n
		outp = True
		
		for i in range(1, n+1):
			# Version only works for psi being id()
			S_lst.append(math.ceil((T - s_sum) / 2))
			s_sum += S_lst[i]
			process_b[i-1] = Process(target=self.par_vf, args=(pp, y[i-1], y[i], S_lst[i], pi[-i]))
			process_b[i-1].start()
		for i in range(1, n+1):
			process_b[i-1].join()
			outp = outp and self.q_vf.get()
		y_res, pi_res = self.evaluate(pp, y[n], T - s_sum)
		outp = outp and (y_in == y_res)
		if outp:
			return "Parallel output accepted"
		else:
			return "Parallel output rejected"
			