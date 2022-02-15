# a small script for the analysis of cycles involving two nodes

import json
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
import csv
import codecs
import math
import random

edge_to_weight = {}
g = nx.DiGraph()

filename_causenet_tsv = '../../data/causenet-precision-without-NUL-lem.tsv'
# with open(filename_causenet_tsv,'r') as f:
with open(filename_causenet_tsv, newline='') as csvfile:
	reader = csv.DictReader(csvfile, delimiter='\t')
	for row in reader:


		s = row['Cause']
		o = row['Effect']
		w = int(row['Weight'])
		edge_to_weight[(s,o)] = w
		if s!=o:
			g.add_edge(s, o)
		# else:
		# 	count_reflexive += 1
		# ct_weight[w] += 1




print('==========================[GE20]=============================')
file_ge5 = "precision_pairs_GE5_random100_annotated.tsv"
gold_standard_file = open(file_ge5, 'r')
reader = csv.DictReader(gold_standard_file, delimiter='\t')

count_correct = 0
count_error = 0
count_unknown = 0

count_annotated = 0

for row in reader:
	s = row["Source"]
	t = row["Target"]
	w_s_t = edge_to_weight[(s,t)]
	w_t_s = edge_to_weight[(t,s)]
	nu = 0
	if w_s_t > w_t_s:
		nu = w_s_t / w_t_s
	else:
		nu = w_t_s / w_s_t

	a = row["Annotation"]
	if nu >= 20:
		if a != 'TBD':
			count_annotated += 1
		if a == 'right':
			if w_s_t > w_t_s:
				count_correct += 1
			else:
				count_error += 1
				print (s, '->', t)
		elif a == 'left':
			if w_s_t < w_t_s:
				count_correct += 1
			else:
				count_error += 1
				print (s, '->', t)
		elif a == 'unknown':
			count_unknown += 1
		else:
			print (a)

print ('total annotated = ', count_annotated)
print ('count correct = ', count_correct, '{:6.2f}%'.format(100*count_correct/count_annotated))
print ('count error = ', count_error, '{:6.2f}%'.format(100*count_error/count_annotated))
print ('count_unknown = ', count_unknown, '{:6.2f}%'.format(100*count_unknown/count_annotated))

print('==========================[GE10]=============================')


file_ge5 = "precision_pairs_GE5_random100_annotated.tsv"
gold_standard_file = open(file_ge5, 'r')
reader = csv.DictReader(gold_standard_file, delimiter='\t')

count_correct = 0
count_error = 0
count_unknown = 0

count_annotated = 0

for row in reader:
	s = row["Source"]
	t = row["Target"]
	w_s_t = edge_to_weight[(s,t)]
	w_t_s = edge_to_weight[(t,s)]
	nu = 0
	if w_s_t > w_t_s:
		nu = w_s_t / w_t_s
	else:
		nu = w_t_s / w_s_t

	a = row["Annotation"]
	if nu >= 10:
		if a != 'TBD':
			count_annotated += 1
		if a == 'right':
			if w_s_t > w_t_s:
				count_correct += 1
			else:
				count_error += 1
				print (s, '->', t)
		elif a == 'left':
			if w_s_t < w_t_s:
				count_correct += 1
			else:
				count_error += 1
				print (s, '->', t)
		elif a == 'unknown':
			count_unknown += 1
		else:
			print (a)

print ('total annotated = ', count_annotated)
print ('count correct = ', count_correct, '{:6.2f}%'.format(100*count_correct/count_annotated))
print ('count error = ', count_error, '{:6.2f}%'.format(100*count_error/count_annotated))
print ('count_unknown = ', count_unknown, '{:6.2f}%'.format(100*count_unknown/count_annotated))


print('==========================[GE5]=============================')


file_ge5 = "precision_pairs_GE5_random100_annotated.tsv"
gold_standard_file = open(file_ge5, 'r')
reader = csv.DictReader(gold_standard_file, delimiter='\t')

count_correct = 0
count_error = 0
count_unknown = 0

count_annotated = 0

for row in reader:
	s = row["Source"]
	t = row["Target"]
	w_s_t = edge_to_weight[(s,t)]
	w_t_s = edge_to_weight[(t,s)]
	nu = 0
	if w_s_t > w_t_s:
		nu = w_s_t / w_t_s
	else:
		nu = w_t_s / w_s_t

	a = row["Annotation"]
	if nu >= 5:
		if a != 'TBD':
			count_annotated += 1
		if a == 'right':
			if w_s_t > w_t_s:
				count_correct += 1
			else:
				count_error += 1
				print (s, '->', t)
		elif a == 'left':
			if w_s_t < w_t_s:
				count_correct += 1
			else:
				count_error += 1
				print (s, '->', t)
		elif a == 'unknown':
			count_unknown += 1
		else:
			print (a)

print ('total annotated = ', count_annotated)
print ('count correct = ', count_correct, '{:6.2f}%'.format(100*count_correct/count_annotated))
print ('count error = ', count_error, '{:6.2f}%'.format(100*count_error/count_annotated))
print ('count_unknown = ', count_unknown, '{:6.2f}%'.format(100*count_unknown/count_annotated))

#
# print('==========================[GE10]=============================')
# ge3_file = open(file_ge3, 'r')
# reader = csv.DictReader(ge3_file, delimiter='\t')
#
# count_right = 0
# count_left = 0
# count_unrelated = 0
# count_unknown = 0
#
# count_annotated = 0
#
# for row in reader:
# 	s = row["Source"]
# 	t = row["Target"]
# 	w_s_t = row["Weight_Source_Target"]
# 	w_t_s = row["Weight_Target_Source"]
# 	a = row["Annotation"]
# 	if int(w_s_t) / int(w_t_s) >= 10:
# 		if a != 'TBD':
# 			count_annotated += 1
# 		if a == 'right':
# 			count_right += 1
# 		elif a == 'left':
# 			count_left += 1
# 		elif  a == 'unknown':
# 			count_unknown += 1
# 		elif  a == 'unrelated':
# 			count_unrelated += 1
# 		else:
# 			pass
#
# print ('total annotated = ', count_annotated)
# print ('count_right = ', count_right, '{:6.2f}%'.format(100*count_right/count_annotated))
# print ('count_left = ', count_left, '{:6.2f}%'.format(100*count_left/count_annotated))
# print ('count_unrelated = ', count_unrelated, '{:6.2f}%'.format(100*count_unrelated/count_annotated))
# print ('count_unknown = ', count_unknown, '{:6.2f}%'.format(100*count_unknown/count_annotated))
#
#
# print('==========================[GE5]=============================')
# ge3_file = open(file_ge3, 'r')
# reader = csv.DictReader(ge3_file, delimiter='\t')
#
# count_right = 0
# count_left = 0
# count_unrelated = 0
# count_unknown = 0
#
# count_annotated = 0
#
# for row in reader:
# 	s = row["Source"]
# 	t = row["Target"]
# 	w_s_t = row["Weight_Source_Target"]
# 	w_t_s = row["Weight_Target_Source"]
# 	a = row["Annotation"]
# 	if int(w_s_t) / int(w_t_s) >= 5:
# 		if a != 'TBD':
# 			count_annotated += 1
# 		if a == 'right':
# 			count_right += 1
# 		elif a == 'left':
# 			count_left += 1
# 		elif  a == 'unknown':
# 			count_unknown += 1
# 		elif  a == 'unrelated':
# 			count_unrelated += 1
# 		else:
# 			pass
#
# print ('total annotated = ', count_annotated)
# print ('count_right = ', count_right, '{:6.2f}%'.format(100*count_right/count_annotated))
# print ('count_left = ', count_left, '{:6.2f}%'.format(100*count_left/count_annotated))
# print ('count_unrelated = ', count_unrelated, '{:6.2f}%'.format(100*count_unrelated/count_annotated))
# print ('count_unknown = ', count_unknown, '{:6.2f}%'.format(100*count_unknown/count_annotated))
#
#
# print('==========================[GE3]=============================')
# ge3_file = open(file_ge3, 'r')
# reader = csv.DictReader(ge3_file, delimiter='\t')
#
# count_right = 0
# count_left = 0
# count_unrelated = 0
# count_unknown = 0
#
# count_annotated = 0
#
# for row in reader:
# 	s = row["Source"]
# 	t = row["Target"]
# 	w_s_t = row["Weight_Source_Target"]
# 	w_t_s = row["Weight_Target_Source"]
# 	a = row["Annotation"]
# 	# if int(w_s_t) / int(w_t_s) >= 5:
# 	if a != 'TBD':
# 		count_annotated += 1
# 	if a == 'right':
# 		count_right += 1
# 	elif a == 'left':
# 		count_left += 1
# 	elif  a == 'unknown':
# 		count_unknown += 1
# 	elif  a == 'unrelated':
# 		count_unrelated += 1
# 	else:
# 		pass
#
# print ('total annotated = ', count_annotated)
# print ('count_right = ', count_right, '{:6.2f}%'.format(100*count_right/count_annotated))
# print ('count_left = ', count_left, '{:6.2f}%'.format(100*count_left/count_annotated))
# print ('count_unrelated = ', count_unrelated, '{:6.2f}%'.format(100*count_unrelated/count_annotated))
# print ('count_unknown = ', count_unknown, '{:6.2f}%'.format(100*count_unknown/count_annotated))
#
# print('===========================[1 - 3]============================')
#
# ge13_file = open(file_3_1, 'r')
# reader = csv.DictReader(ge13_file, delimiter='\t')
#
# count_right = 0
# count_left = 0
# count_unknown = 0
# count_annotated = 0
#
# for row in reader:
# 	s = row["Source"]
# 	t = row["Target"]
# 	w_s_t = row["Weight_Source_Target"]
# 	w_t_s = row["Weight_Target_Source"]
# 	a = row["Annotation"]
# 	if a != 'TBD':
# 		count_annotated += 1
# 	if a == 'right':
# 		count_right += 1
# 	elif a == 'left':
# 		count_left += 1
# 	elif  a == 'unknown':
# 		count_unknown += 1
# 	elif  a == 'unrelated':
# 		count_unrelated += 1
# 	else:
# 		pass
#
# print ('total annotated = ', count_annotated)
# print ('count_right = ', count_right, '{:6.2f}%'.format(100*count_right/count_annotated))
# print ('count_left = ', count_left, '{:6.2f}%'.format(100*count_left/count_annotated))
# print ('count_unrelated = ', count_unrelated, '{:6.2f}%'.format(100*count_unrelated/count_annotated))
# print ('count_unknown = ', count_unknown, '{:6.2f}%'.format(100*count_unknown/count_annotated))
