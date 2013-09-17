#!/usr/bin/env python2
from ah import getfilenames
import numpy as np
import cPickle

def main():
	Y = np.zeros((38,836))
	filenames = getfilenames('blur')
	vector=[]
	for f in filenames:
		f = f.split('/')[-1]
		index = int(f[5:7])
		if index>14: index-=1
		index-=1
		vector.append(index)
	for i in range(836):
		print i
		tmp = np.zeros(38)
		tmp[vector[i]] = 1
		Y[:,i] = tmp
	cPickle.dump(Y, open('Y.cpickle', 'wb'))
if __name__ == '__main__':
	main()
