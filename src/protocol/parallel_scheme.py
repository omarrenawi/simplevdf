from prover import *
from verifier import *
from multiprocessing import Process, Queue 


class Parallel_scheme():
	# weakly efficient and self-composable VDF
	def __init__(self, psi, T, setup, gen, eval, vf):
		self.psi = psi
		self.T = T
		
		self.setup = setup
		self.gen = gen 
		self.eval = eval
		self.vf = vf
		self.prove = # TODO
		self.comp = # TODO
		
	def par_prove(a, q):
		q.put(self.prove(a))
	
	def par_vf(pp, y_i_1, y_i, S_i, q):
		q.put(self.vf(pp, y_i_1, y_i, S_i]))
	
		
	def setup_(lambd):
		return self.setup(lambd)
	
	def gen_(pp):
		return self.gen(pp)
	
	def eval_(pp, x, T, S = 0, fst = True):
		# multiprocessing queue to add π
		q= Queue()
		if fst:
			while (True):
				if (S + self.psi(S) >= T): break
			else: S += 1
		if (S <= 1):
			y, alpha = Comp(pp, x, T)
			return (y, set())
		else:
			y, alpha = Comp(pp, x, S) 
			# spawn the parallel thread
			process_pi = Process(target=par_prove, args=(alpha, q,))
			process_pi.start()
			y_ , L = eval_(pp, y, T-S)
			process_pi.join()
			pi = q.get()
			return (y_, L.insert(0, (y, pi)))
			
	def vf_(pp, x, y_in, pi, T):
		# multiprocessing queue to add b_i
		q= Queue()
		y = []
		y.add(x);
		pi = []	
		for ((fst, snd) in pi):			# parse pi into list of n y[i],pi[i] tupels
			y.add(fst)
			pi.add(snd)
		S_lst = []
		b_lst = []
		S_lst[0] = T
		b = [None] * n
		outp = True
		
		for i in range(1, n+1):
			S_lst.append(0) # ? smallest integer, dont know about negativity
			s_sum = 0
			for j in range(1, i):
				s_sum += S_lst[j]
			while((S_lst[i] + self.psi(S_lst[i])) < (S_lst[0] - s_sum)):
				S_lst[i] += 1
			process_b[i-1] = Process(target=par_vf, args=(pp, y[i-1], y[i], S_lst[i],))
			process_b[i-1].start()
			b_lst.append(thread.start_new_thread(self.vf, (pp, y[i-1], y[i], S_lst[i])))
		for i in range(1, n+1):
			process_b[i-1].join()
			outp = outp and q.get()
		s_sum = 0
		for j in range(1, n+1):
			s_sum += S_lst[j]
		y_res, pi_res = self.eval(pp, y[n], T - s_sum)
		outp = outp and (y_in == y_res)
		return outp	
			
			