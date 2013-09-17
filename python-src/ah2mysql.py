#!/usr/bin/env python2
import sqltools2
import numpy as np
conn, cur = sqltools2.connect()
def insert(ah59x760,cur, index):
	for i in range(59):
		sql = 'insert into ah3 values(%d, %d'%(index, i)
		for j in range(760):
			sql += ',%d'%ah59x760[i,j]
		sql+=')'
		cur.execute(sql)

ah = data
indexarray = np.arange(0,760*322,322)
for i in range(322):
	print i
	tmp = ah[:,indexarray]
	indexarray+=1
	insert(tmp, cur, i)

sqltools2.disconnect(conn, cur)
