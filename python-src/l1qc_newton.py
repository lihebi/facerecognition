#!/usr/bin/env python2
from numpy import ceil, log, dot
from cvxopt import matrix
import numpy as np
from numpy import sqrt
from cvxopt.lapack import gesv as linsolve
from time import time as curtime
def l1qc_newton(x0, u0, A, b, epsilon, tau, newtontol, newtonmaxiter):
	alpha = 0.01
	beta = 0.5
	AtA = dot(A.T, A)#0.05s
	x = x0
	u = u0
	r = dot(A,x) - b
	fu1 = x - u
	fu2 = -x - u
	fe = 1./2*(dot(r.T,r)-epsilon**2)
	f = sum(u) - (1./tau)*(sum(log(-fu1)) + sum(log(-fu2)) + log(-fe))
	niter = 0
	done = 0
	while not done:
		t = curtime()
		atr = dot(A.T,r)
		ntgz = 1./fu1 - 1./fu2 + 1./fe*atr
		ntgu = -tau - 1./fu1 -1./fu2
		gradf = -(1./tau)*np.vstack((ntgz.reshape(-1,1), ntgu.reshape(-1,1)))
		sig11 = 1./fu1**2 + 1./fu2**2
		sig12 = -1./fu1**2 + 1./fu2**2
		sigx = sig11 - 1.*sig12**2/sig11
		w1p = ntgz - (1.*sig12/sig11)*ntgu
		H11p = np.diag(sigx) - (1./fe)*AtA + (1./fe)**2*dot(atr,atr.T)
		w1p.shape = -1,1
		dx = np.linalg.solve(H11p, w1p)
		dx = dx.flatten()
		Adx = dot(A, dx)
		du = 1./sig11*ntgu-1.*sig12/sig11*dx
		ifu1 = (dx-du>0)
		ifu2 = (-dx-du>0)
		aqe = dot(Adx.T, Adx)
		bqe = dot(2*r.T, Adx)
		cqe = dot(r.T, r) - epsilon**2
		aa = -fu1[ifu1]/(dx[ifu1]-du[ifu1])
		bb = -fu2[ifu2]/(-dx[ifu2]-du[ifu2])
		cc = (-bqe+sqrt(bqe**2-4*aqe*cqe))/(2*aqe)
		cc = cc.flatten()
		tmp = np.hstack((aa,bb,cc))
		smax = min(1, min(tmp))
		s = 0.99*smax
		suffdec = 0
		backiter = 0
		gradf = gradf.flatten()
		while not suffdec:
			xp = x + s*dx
			up = u + s*du
			rp = r + s*Adx
			fu1p = xp - up
			fu2p = -xp - up
			fep = 1./2*(dot(rp.T, rp) - epsilon**2)
			fp = sum(up) - (1/tau)*(sum(log(-fu1p)) + sum(log(-fu2p)) + log(-fep))
			tmp = np.hstack((dx, du))
			tmp = dot(gradf, np.hstack((dx, du)))
			flin = f + alpha*s*tmp
			suffdec = (fp<=flin)
			s = beta*s
			backiter = backiter+1
		x = xp
		u = up
		r = rp
		fu1 = fu1p
		fu2 = fu2p
		fe = fep
		f = fp
		lambda2 = -dot(gradf, np.hstack((dx, du)))
		stepsize = s*np.linalg.norm(np.hstack((dx, du)))
		niter = niter+1
		print niter,
		done = (lambda2/2 < newtontol) | (niter >= newtonmaxiter)
		print (lambda2/2), newtontol
	return [xp, up, niter]
def main():
	pass

if __name__ == '__main__':
	main()
