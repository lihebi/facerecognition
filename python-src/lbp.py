#!/usr/bin/env python2
import numpy as np
from numpy import pi, ceil, floor, sin, cos
from time import time as curtime

def lbp(matrix):
	radius = 1
	neighbors = 8
	d_matrix = np.double(matrix)
	a = 2*pi/neighbors
	spoints = np.zeros((neighbors, 2))
	for i in range(neighbors):
		spoints[i,0]=-radius*sin(i*a)
		spoints[i,1]= radius*cos(i*a)
	ysize,xsize = matrix.shape
	miny = min(spoints[:,0])
	maxy = max(spoints[:,0])
	minx = min(spoints[:,1])
	maxx = max(spoints[:,1])
	bsizey=ceil(max(maxy,0))-floor(min(miny,0))+1;
	bsizex=ceil(max(maxx,0))-floor(min(minx,0))+1;
	origy=1-floor(min(miny,0));
	origx=1-floor(min(minx,0));
	if xsize < bsizex or ysize < bsizey:
		print 'ill'
	dx = xsize - bsizex;
	dy = ysize - bsizey;
	C = matrix[origy-1:origy+dy,origx-1:origx+dx];
	d_C = np.double(C);
	bins = 2^neighbors;
	result=np.zeros((dy+1,dx+1));
	for i in range(neighbors):
		y = spoints[i,0]+origy
		x = spoints[i,1]+origy
		fy = floor(y); cy = ceil(y); ry = round(y);
		fx = floor(x); cx = ceil(x); rx = round(x);
		if (abs(x - rx) < 1e-6) and (abs(y - ry) < 1e-6):
			N = matrix[ry-1:ry+dy,rx-1:rx+dx];
			D = (N >= C)*1;
		else:
			ty = y - fy;
			tx = x - fx;
			w1 = (1 - tx) * (1 - ty);
			w2 =      tx  * (1 - ty);
			w3 = (1 - tx) *      ty ;
			w4 =      tx  *      ty ;
			N = w1*d_matrix[fy-1:fy+dy,fx-1:fx+dx] + w2*d_matrix[fy-1:fy+dy,cx-1:cx+dx] + w3*d_matrix[cy-1:cy+dy,fx-1:fx+dx] + w4*d_matrix[cy-1:cy+dy,cx-1:cx+dx]
			D = N >= d_C;
		v = 2**i;
		result = result+v*D
	mapping = genmapping()
	x,y = result.shape
	for i in range(x):
		for j in range(y):
			result[i,j] = mapping[int(result[i,j])]
	result=np.histogram(result.reshape(1,-1),range(60))[0];
	result.shape = (59,1)
	return result
def genmapping():
	num = 8
	table = range(2**num)
	index=0
	for i in range(2**num):
		tmp = (i<<1 & 1<<8)>>8
		j = (i<<1 | tmp)&255
		numt = sumbit(i^j)
		if numt<=2:
			table[i]=index
			index+=1
		else:
			table[i]=58
	return table
def sumbit(num):
	tmp=0
	for i in range(8):
		tmp+=num&1
		num = num>>1
	return tmp
if __name__ == '__main__':
	result = lbp(matrix)
