#!/usr/bin/env python2
import cPickle
import numpy as np
def weaklearner(feature, y, weight):
	cntSamples = len(feature)
	u1 = np.mean(feature[y==1])
	u2 = np.mean(feature[y==0])
	iteration = 4
	sectNum = 8
	maxFea = max(u1,u2)
	minFea = min(u1,u2)
	step = (maxFea-minFea)/(sectNum-1)
	bestError = cntSamples
	for iter in range(iteration):
		tempError = cntSamples
		for i in range(sectNum):
			thresh = minFea+i*step
			h = feature<thresh
			errorrate = sum(weight[h^(y==1)])
			p=1
			if errorrate>0.5:
				errorrate = 1-errorrate
				p=-1
			if errorrate<bestError:
				bestError=errorrate
				bestThresh = thresh
				bestBias = p
		span = (maxFea-minFea)/8
		maxFea=bestThresh+span
		minFea=bestThresh-span
		step=(maxFea-minFea)/(sectNum-1)
	return [bestError, bestThresh, bestBias]
def train(rhs, y, weight, minError):
	for index in range(322):
		print index
		rh = rhs[index+1]# 38x836
		feature = rh.flatten()
		tmpError, tmpThresh, tmpBias = weaklearner(feature, y, weight)
		if tmpError<minError:
			minError=tmpError
			print '\t',
			print minError
			tmp=[tmpThresh, tmpBias, index]
	return tmp
def main():
	#rhs = cPickle.load(open('rhs.cpickle','rb'))
	#Y = cPickle.load(open('Y.cpickle','rb'))
	global rhs, Y
	Y = Y.flatten()
	T=10
	cntSamples = rhs[1].shape[0]*rhs[1].shape[1]
	weight = np.zeros(cntSamples)
	weight[Y==1] = 1./(2*len(weight[Y==1]))
	weight[Y==0] = 1./(2*len(weight[Y==0]))
	Hypothesis = {}
	AlphaT = np.zeros(T)
	for t in range(T):
		weight = weight/sum(weight)
		minError = cntSamples
		Hypothesis[t] = train(rhs, Y, weight, minError)
		h = weaklearnerClassify(rhs, Y, weight, Hypothesis[t])
		wrongArray = h^(Y==1)
		errorRate = sum(weight[wrongArray])
		weight[wrongArray] *= 1.2#(1-errorRate)/errorRate
if __name__ == '__main__':
	main()
