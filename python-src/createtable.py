#!/usr/bin/env python2
import sqltools2
conn, cur = sqltools2.connect()
sql = 'create table bh4(class int, id int'
for i in range(836):
	sql += ', d%d int'%i
sql += ')'
cur.execute(sql)

sqltools2.disconnect(conn, cur)
