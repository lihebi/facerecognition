#!/usr/bin/env python2
writer = open('out.txt', 'w')
for line in open('log115to127.txt'):
	if not line.startswith(','):
		writer.write(line)
