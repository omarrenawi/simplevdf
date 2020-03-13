from prover import *
from verifier import *
from multiprocessing import Process, Queue, Manager


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
		
	def psi(self, x):
		return x
			
	def par_prove(self, N, x, T, y, pr):
		pr.put(self.prove(N, x, T, y))
	
	def par_prove_alpha(self, alpha):
		self.q_eval.put(self.prove(alpha))
	
	def par_vf(self, pp, y_i_1, y_i, S_i, pi_i):
		self.q_vf.put(self.vf(pp, y_i_1, y_i, S_i, pi_i)) 
	
		
	def setup_(self, lambd):
		return self.setup(lambd)
	
	def gen_(self, pp):
		return self.gen(pp)
	
	def eval_(self, pp, x, T):
		# only works for psi(S) = S
		S = math.ceil(T / 2)
		if (S <= 1):
			y, alpha = self.evaluate(pp, x, T)
			return (y, self.L_init)
		else:
			pr = Queue()
			y = self.comp(pp, x, S)
			process_pi = Process(target=self.par_prove, args=(pp, x, S, y, pr))
			process_pi.start()
			y_ , L = self.eval_(pp, y, T - S)
			process_pi.join()
			pi = pr.get()
			L.insert(0, (y, pi))
			return (y_, L)
			
	def vf_(self, pp, x, y_in, pi_in, T):
		n = 0
		y = []
		pi = []	
		y.append(x);
		pi.append(x); 			# pi[0] is not used/needed anyway
		for el in pi_in:		# parse pi into list of n y[i],pi[i] tupels
			fst, snd = el
			y.append(fst)
			pi.append(snd)
			n += 1
		S_lst = [None] 
		s_sum = 0
		S_lst[0] = T
		process_b = [None] * n
		outp = True
		
		for i in range(1, n+1):
			# only works for psi(S) = S
			S_lst.append(math.ceil((T - s_sum) / 2))
			s_sum += S_lst[i]
			process_b[i-1] = Process(target=self.par_vf, args=(pp, y[i-1], y[i], S_lst[i], pi[i]))
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
			