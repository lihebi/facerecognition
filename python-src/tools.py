#!/usr/bin/env python2
from imports import *
from consts import *

def getfilenames(dir):
	#{{{
	dir = YALEB_DIR+dir
	ret = []
	for root,dirs,files in os.walk(dir):
		files.sort()
		for f in files:
			ret.append(dir+'/'+f)
	return ret
#}}}
def genPatchesFromXY(x,y):
	#{{{
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
#}}}
def genPatches(xs,ys):
	#{{{
	patches = []
	for x in xs:
		for y in ys:
			patches += genPatchesFromXY(x,y)
	return patches
#}}}
def getHfromdb(cur, table, index):
	#{{{
	H = np.array([])
	cur.execute('select * from %s where class=%d'%(table, index))
	for r in cur.fetchmany(1000):
		tmp = r[2:]
		if len(H)>0:
			H = np.vstack((H, tmp))
		else:
			H = tmp
	return H#}}}
def calLBPForSingleImage(matrix):
	#{{{
	wholelbp=np.zeros((59,322))
	patches = genPatches()
	count=0
	for patch in patches:
		matrixtmp = matrix[patch['xstart']:patch['xend']+1, patch['ystart']:patch['yend']+1]
		_lbp = lbp(matrixtmp)
		wholelbp[:,count] = _lbp.T
		count+=1
	return wholelbp#}}}
def calLBPForSinglePatch(imageset, index):
	#{{{
	patch = genPatches()[index]
	wholelbp = np.zeros((59,0))
	for f in imageset:
		print f
		data = getImageData(f)
		if index!=-1:
			matrixtmp = data[patch['xstart']:patch['xend']+1, patch['ystart']:patch['yend']+1]
		else:
			matrixtmp = data
		_lbp = lbp(matrixtmp)
		wholelbp = np.hstack((wholelbp, _lbp))
	return wholelbp#}}}
def calH(name):
	#{{{
	tahs = []
	ahs = []
	if name=='A':
		trainingset = getfilenames('training')
	else:
		trainingset = getfilenames('blur')
	for filename in trainingset:
		img = Image.open(filename)
		vector= calNewForSingleImage(img)
		tahs.append(vector)
	for index in range(tahs[0].shape[1]):
		vect = np.array([])
		for count in range(len(tahs)):
			tmp = tahs[count][:,index]
			if len(vect)>0:
				vect = np.vstack((vect, tmp))
			else:
				vect = tmp
		vect = vect.T
		ahs.append(vect)
	return ahs#}}}
def calNewForSingleImage(img):
	#{{{
	patches = genPatches([48,96,192],[56,168])
	result = np.array([])
	for patch in patches:
		box = (patch['ystart'], patch['xstart'], patch['yend']+1, patch['xend']+1)
		imgtmp = img.crop(box)
		vector = calNew(imgtmp)
		if len(result)>0:
			result = np.vstack((result, vector))
		else:
			result = vector
	return result.T#}}}
def calNew(img):
	#{{{
	img = img.resize((6,3))
	data = img.getdata()
	data = np.array(data)
	return data.flatten()#}}}
def insertintodb(cur, table, data):
	sql='insert into %s values('%table
	for i in data:
		sql += str(i)+','
	sql = sql[:-1]+')'
	cur.execute(sql)
