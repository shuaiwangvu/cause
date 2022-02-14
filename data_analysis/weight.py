# this is a script for the analysis of the weight in the original file
# there are two plots:
# 1. a plot of weights and its frequency.
# 2. a plot of difference in weights in cycles of two entities.

# export the pairs in cycles with two nodes.
import json
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
import csv
import codecs
import math
import random

ct_sources = Counter()
ct_weight = Counter()
ct_scc = Counter()
edge_to_weight = {}

g = nx.DiGraph()
count_0 = 0
count = 0
weight_proportion = []
filename_causenet_tsv = 'causenet-full-without-NUL.tsv'

count_reflexive = 0

filename_causenet_tsv = '../../data/causenet-precision-without-NUL-lem.tsv'
# with open(filename_causenet_tsv,'r') as f:
with open(filename_causenet_tsv, newline='') as csvfile:
	reader = csv.DictReader(csvfile, delimiter='\t')
	for row in reader:

	# for line in f.readlines():
		count += 1
		if count %1000000 == 0:
			# break
			print ('processed: ', count)

		s = row['Cause']
		o = row['Effect']
		w = int(row['Weight'])
		edge_to_weight[(s,o)] = w
		if s!=o:
			g.add_edge(s, o)
		else:
			count_reflexive += 1
		ct_weight[w] += 1

print ('count_0 = ', count_0)
print ('The graph has ', g.number_of_nodes(), ' nodes')
print ('The graph has ', g.number_of_edges(), ' edges')
print ('\t with ', count_reflexive, ' reflexive edges')

fig, axs = plt.subplots(2)
# axs[0].set_title('in-degree')
# axs[1].set_title('out-degree')
fig.set_figwidth(6)
fig.set_figheight(8)

axs[0].spines['top'].set_visible(False)
axs[0].spines['right'].set_visible(False)
axs[0].autoscale(tight=True)

x = ct_weight.keys()
y = ct_weight.values()
print ('the max weight: ', max(x))
axs[0].scatter(x, y, alpha = 0.3)
axs[0].set_yscale('log')
# axs[0].set_xscale('log')
axs[0].set_xlabel('weight')
axs[0].set_ylabel('frequency')

# sccs = nx.strongly_connected_components(g)
# sccs_two = []
# for scc in sccs:
# 	if len(scc) == 2:
# 		sccs_two.append(scc)

sccs_two = []

for (s, t) in g.edges():
	w_s_t = edge_to_weight [(s,t)]
	if (t, s) in g.edges():
		w_t_s = edge_to_weight [(t,s)]
		w_big = 0
		w_small = 0
		sccs_two.append(set([s, t]))


ge_five = open ("lem_pairs_GE5.tsv", "w")
between_five_one = open ("pairs_5_1.tsv", "w")
eq_one = open ("pairs_eq.tsv", "w")

ge_five.write('Source\tTarget\tWeight_Source_Target\tWeight_Target_Source\tAnnotation\n')
between_five_one.write('Source\tTarget\tWeight_Source_Target\tWeight_Target_Source\tAnnotation\n')
eq_one.write('Source\tTarget\tWeight_Source_Target\tWeight_Target_Source\tAnnotation\n')

pairs_ge5 = set()

for scc in sccs_two:
	(s, t) = scc
	w_s_t = edge_to_weight [(s,t)]
	w_t_s = edge_to_weight [(t,s)]
	w_big = 0
	w_small = 0
	if w_s_t > w_t_s:
		w_big = w_s_t
		w_small = w_t_s
		weight_proportion.append(w_s_t / w_t_s)
	elif w_s_t < w_t_s:
		weight_proportion.append(w_t_s / w_s_t)
		w_big = w_t_s
		w_small = w_s_t
	else:
		w_small = w_s_t
		w_big = w_t_s
		weight_proportion.append(1)

	nu = w_big / w_small
	if nu >= 5:
		ge_five.write(str(s)+'\t'+ str(t) +'\t'+ str(w_s_t)+ '\t'+ str(w_t_s)+ '\tTBD\n')
		pairs_ge5.add((s,t))
	elif nu < 5 and nu > 1:
		between_five_one.write(str(s)+'\t'+ str(t) +'\t'+ str(w_s_t)+ '\t'+ str(w_t_s) + '\tTBD\n')
	elif nu <= 1:
		eq_one.write(str(s)+'\t'+ str(t) +'\t'+ str(w_s_t)+ '\t'+ str(w_t_s) + '\tTBD\n')



ge_five = open ("precision_pairs_GE5_random100.tsv", "w")
ge_five.write('Source\tTarget\tAnnotation\n')

for (s, t) in random.sample(list(pairs_ge5), k=100):
	w_s_t = edge_to_weight [(s,t)]
	w_t_s = edge_to_weight [(t,s)]
	ge_five.write(str(s)+'\t'+ str(t) +'\tTBD\n')

# ge_five = open ("pairs_GE3.tsv", "w")
# between_five_one = open ("pairs_3_1.tsv", "w")
# eq_one = open ("pairs_1.tsv", "w")

print ('There are in total ', len (sccs_two), ' cycles with two nodes')
print ('There are in total ', len (weight_proportion), ' cycles with two nodes')

filtered = list(filter(lambda score: score >= 20, weight_proportion))
print ('\n>= 20', len (filtered))
print (' proportion: {:6.2f}%'.format(100*len(filtered)/len(weight_proportion)))

filtered = list(filter(lambda score: score >= 10, weight_proportion))
print ('\n>= 10', len (filtered))
print (' proportion: {:6.2f}%'.format(100*len(filtered)/len(weight_proportion)))


filtered = list(filter(lambda score: score >= 5, weight_proportion))
print ('\n>= 5', len (filtered))
print (' proportion: {:6.2f}%'.format(100*len(filtered)/len(weight_proportion)))


filtered = list(filter(lambda score: score >= 3, weight_proportion))
print ('\n>= 3', len (filtered))
print (' proportion: {:6.2f}%'.format(100*len(filtered)/len(weight_proportion)))

filtered = list(filter(lambda score: score < 3 and score > 1, weight_proportion))
print ('1 < x <3', len (filtered))
print (' proportion: {:6.2f}%'.format(100*len(filtered)/len(weight_proportion)))

filtered = list(filter(lambda score: score == 1, weight_proportion))
print ('1 == x', len (filtered))
print (' proportion: {:6.2f}%'.format(100*len(filtered)/len(weight_proportion)))

filtered = list(filter(lambda score: score < 1, weight_proportion))
print (' x < 1 ', len (filtered))
print (' proportion: {:6.2f}%'.format(100*len(filtered)/len(weight_proportion)))

print('the maximum weight difference: ',max(weight_proportion))
# weight_proportion
n_bins = 100
weight_proportion = [math.log10(w) for w in weight_proportion]


axs[1].hist(weight_proportion, bins=n_bins)
# axs[1].set_xscale('log')
# axs[1].set_yscale('log')
axs[1].set_xlabel(r"$log_{10}\nu$") # weight difference
axs[1].set_ylabel('frequency')

plt.savefig('weight_statistics_precision.png', bbox_inches='tight', dpi = 300)



# >= 20 2419
#  proportion:   5.12%
#
# >= 10 5058
#  proportion:  10.70%
#
# >= 5 10147
#  proportion:  21.47%
#
# >= 3 16405
#  proportion:  34.71%
# 1 < x <3 11123
#  proportion:  23.53%
# 1 == x 19738
#  proportion:  41.76%
#  x < 1  0
#  proportion:   0.00%
