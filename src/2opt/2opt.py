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
	best_path = cost(m, d, f)
	size = len(m)
	i = 0
	#print m
	for i in range(0, size-1):
		for j in range(i+1, size):
			posI = m.index(i)
			posJ = m.index(j)
			m[posI] = j
			m[posJ] = i
			current_path = cost(m, d, f)
			if(current_path < best_path):
				best_matching = copy(m)
				best_path = current_path
	print 'final solution: ', best_matching
	print 'final cost: ', best_path

def get_minor(list, n):
	for i in range(0, n):
		if i not in list:
			return i
	return None

def read_file():
	ins = open(constants.FILE_NAME, "r" )
	
	i = 0
	br = 0

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

# greedy algorithm to generate initial solution
def initial_solution(distance, flow):
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
			best_cost = cost(m, distance, flow)
			if j == 0:
				best_cost_final = best_cost
			for i in range(0, n):
				if i not in m:
					m2[len(m2)-1] = i
					c = cost(m2, distance, flow)
					if c < best_cost:
						m[len(m)-1] = i
						best_cost = c
			j = j + 1

		if best_cost < best_cost_final:
			best_cost_final = best_cost
			m_final = copy(m)

		m_x.append(m)

	# check the best greedy initial solution, considering solutions starting with 0, 1, 2 .. n
	b_array = copy(m_x[0])
	b_cost = cost(b_array, distance, flow)

	for i in range(1, n):
		cus = cost(m_x[i], distance, flow)
		if cus < b_cost:
			b_cost = cus
			b_array = copy(m_x[i])

	print 'initial solution: ', b_array
	print 'initial cost: ', b_cost

	return b_array

distance = []
flow = []
read_file()
initial_matching = initial_solution(distance, flow)
iteration(initial_matching, distance, flow)