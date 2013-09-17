#!/usr/bin/env python2
from imports import *
from tools import *
from consts import *
from termcolor import colored
def main():
	ahs = cPickle.load(open('ahs.cpickle','rb'))
	bhs = cPickle.load(open('bhs.cpickle','rb'))
	ah = np.double(ahs[-1])
	bh = np.double(bhs[-1])
	li = bh[:,100]
	x0 = np.dot(ah.T, li)
	xp = l1qc_logbarrier(x0,ah,li,0.01)
	plt.plot(xp)
	plt.show()
if __name__ == '__main__':
	conn, cur = sqltools2.connect()
	main()
	sqltools2.disconnect(conn, cur)
