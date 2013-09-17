#!/usr/bin/env python2
import numpy as np
from l1qc_newton import l1qc_newton
from cvxopt.lapack import gesv as linsolve
from cvxopt import matrix
from numpy import ceil, log, dot
from time import time as curtime
def l1qc_logbarrier(x0, A, b, epsilon):
	#lbtol = 1e-3
	lbtol = 0.1
	mu = 10
	newtontol = lbtol
	newtonmaxiter = 50
	N = x0.shape[0]
	if np.linalg.norm(dot(A,x0)-b)>epsilon:
		w = np.linalg.solve(dot(A,A.T), b)
		x0 = dot(A.T, w)
	x = x0
	u = 0.95*abs(x0) + 0.1*max(abs(x0))
	tau = max((2*N+1)/sum(abs(x0)), 1)
	lbiter = ceil((log(2*N+1)-log(lbtol)-log(tau))/log(mu))
	totaliter = 0
	for i in range(int(lbiter)):
		print '='*100
		xp, up, ntiter = l1qc_newton(x, u, A, b, epsilon, tau, newtontol, newtonmaxiter)
		totaliter = totaliter + ntiter
		x = xp
		u = up
		tau = mu*tau
	return xp
