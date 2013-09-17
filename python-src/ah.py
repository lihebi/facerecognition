#!/usr/bin/env python2
import Image, os, cPickle
import numpy as np
from time import time as curtime
from math import pi, floor, ceil
from lbp import lbp

def getImageData(filename):
#	image = Image.open('./YaleB/training/yaleB10_P00A-025E+00.pgm')
	image = Image.open(filename)
	data = image.getdata()
	data = np.array(data)
	data.shape = 192,168
	return data
def getfilenames(dirname):
	wholedirname = '/home/hebi/YaleB/'+dirname
	result = []
	for root, dirs, files in os.walk(wholedirname):
		files.sort()
		for f in files:
			result.append(wholedirname+'/'+f)
	return result
def genPatches():
	xs = [24,48,96]
	ys = [12,28,56]
	patches = []
	for x in xs:
		for y in ys:
			patches += genPatchesFromXY(x,y)
	return patches
def genPatchesFromXY(x,y):
	patches = []
	for i in np.linspace(0,192,192/x, endpoint=False):
		for j in np.linspace(0,168,168/y, endpoint=False):
			i=int(i)
			j=int(j)
			patch = {}
			patch['xstart']	=i
			patch['xend']	=i+x-1
			patch['ystart']	=j
			patch['yend']	=j+y-1
			patches.append(patch)
	return patches
def calLBP(imageset):
	ah = np.zeros((59,1))
	count=0
	for filename in imageset:
		t = curtime()
		count+=1
		print count
		matrix = getImageData(filename)
		vect59x322 = calLBPForSingleImage(matrix)
		ah = np.hstack((ah, vect59x322))
		print curtime()-t
	ah = ah[:,1:]
	return ah
def  calLBPForSingleImage(matrix):
	wholelbp=np.zeros((59,322))
	patches = genPatches()
	count=0
	for patch in patches:
		matrixtmp = matrix[patch['xstart']:patch['xend']+1, patch['ystart']:patch['yend']+1]
		_lbp = lbp(matrixtmp)
		wholelbp[:,count] = _lbp.T
		count+=1
	return wholelbp
def bh():
	blurset = getfilenames('blur')
	bh = calLBP(blurset)
	cPickle.dump(bh, open('bh.cpickle', 'wb'))

def main():
	trainingset = getfilenames('training')
	ah = calLBP(trainingset)
	cPickle.dump(ah, open('ah.cpickle','wb'))

if __name__ == '__main__':
	#main()
	bh()
