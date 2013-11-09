# QAP problem
# 2-opt heuristic
# author: Daniel Gribel -- daniel.gribel@uniriotec.br

from copy import copy, deepcopy
from random import randint
import math
import constants
import re

def cost(matching, d, f):
	total = 0
	size = len(matching)
	for i in range(0, size-1):
		total = total + get(matching[i], matching[i+1], f) * get(i, i+1, d)
		print 'total: ', total
	total = total + get(matching[size-1], matching[0], f) * get(size-1, 0, d)
	return total

def cost2(matching, d, f):
	total = 0
	size = len(matching)
	for i in range(0, size):
		for j in range(0, size):
			if i != j:
				x = get(matching[i], matching[j], f) * get(i, j, d)
				total = total + x
	return total

def get(first, second, array):
	return array[ int(math.sqrt(len(array))) * first + second]

def iteration(m, d, f):
	best_matching = []
	best_matching = copy(m)
	best_path = cost2(m, d, f)
	size = len(m)
	i = 0
	#print m
	for i in range(0, size-1):
		for j in range(i+1, size):
			posI = m.index(i)
			posJ = m.index(j)
			m[posI] = j
			m[posJ] = i
			current_path = cost2(m, d, f)
			if(current_path < best_path):
				best_matching = copy(m)
				best_path = current_path
	print 'final solution: ', best_matching
	print 'final cost: ', best_path

ins = open(constants.FILE_NAME, "r" )
distance = []
flow = []

i = 0
br = 0

# for line in ins:
# 	if i == 0:
# 		n = line.split("\n")[0]
# 	elif line == "\n":
# 		br += 1
# 	else:
# 		if br == 1:
# 			for k in line.split(" "):
# 				distance.append( int(k.split("\n")[0]) )
# 		if br == 2:
# 			for k in line.split(" "):
# 				flow.append( int(k.split("\n")[0]) )
# 	i += 1

for line in ins:
	if i == 0:
		n = line.split("\n")[0]
	elif line == "\n":
		br += 1
	else:
		if br == 1:
			for k in re.split(' +', line):
				if k != '':
					distance.append( int(k.split("\n")[0]) )
		if br == 2:
			for k in re.split(' +', line):
				if k != '':
					flow.append( int(k.split("\n")[0]) )
	i += 1

def get_minor(list, n):
	for i in range(0, n):
		if i not in list:
			return i
	return None

# greedy algorithm to generate initial solution
n = int(math.sqrt(len(distance)))
best_cost_final = 0
m_x = []

for q in range(0, n):
	m = [q]
	m2 = [q]
	j = 0
	while j < n-1:
		k = get_minor(m, n)
		m.append(k)
		m2 = copy(m)
		best_cost = cost2(m, distance, flow)
		if j == 0:
			best_cost_final = best_cost
		for i in range(0, n):
			if i not in m:
				m2[len(m2)-1] = i
				c = cost2(m2, distance, flow)
				if c < best_cost:
					m[len(m)-1] = i
					best_cost = c
		j = j + 1

	if best_cost < best_cost_final:
		best_cost_final = best_cost
		m_final = copy(m)

	m_x.append(m)

b_array = copy(m_x[0])
b_cost = cost2(b_array, distance, flow)

for i in range(1, n):
	cus = cost2(m_x[i], distance, flow)
	if cus < b_cost:
		b_cost = cus
		b_array = copy(m_x[i])

print 'initial solution: ', b_array
print 'initial cost: ', b_cost
iteration(b_array, distance, flow)