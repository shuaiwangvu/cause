# this is a small test for the causenet-precision.jsonl file
# The precision graph has
# The graph has  80223  nodes
# The graph has  197806  edges

# Strongly connected component
# the biggest scc has  7724 nodes
# Counter({1: 72469, 2: 15, 7724: 1})

import json
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
import csv
import codecs

ct_sources = Counter()
ct_weight = Counter()
ct_scc = Counter()
count = 0

g = nx.DiGraph()
count_0 = 0
count = 0
# filename_causenet_tsv = 'causenet-full-without-NUL.tsv'
filename_causenet_tsv = '../../data/causenet-precision-without-NUL-lem.tsv'



# with open(filename_causenet_tsv,'r') as f:

with open(filename_causenet_tsv, newline='') as csvfile:
	reader = csv.DictReader(csvfile, delimiter='\t')
	for row in reader:
		# print(row['first_name'], row['last_name'])
	# reader = csv.reader(f, delimiter='\t')
	# for row in reader:
	# # Cause
	# # Effect
	# # Weight
	# # for line in f.readlines():
		count += 1
		if count %10000 == 0:
			# break
			print ('processed: ', count)

		# row = line.split('\t')
		s = row['Cause']
		o = row['Effect']
		w = int(row['Weight'])
		g.add_edge(s, o)
		ct_weight[w] += 1

print ('count_0 = ', count_0)
print ('The graph has ', g.number_of_nodes(), ' nodes')
print ('The graph has ', g.number_of_edges(), ' edges')

# fig, axs = plt.subplots(2)
# # axs[0].set_title('in-degree')
# # axs[1].set_title('out-degree')
# fig.set_figwidth(6)
# fig.set_figheight(10)
#
# axs[0].spines['top'].set_visible(False)
# axs[0].spines['right'].set_visible(False)
# axs[0].autoscale(tight=True)
#
# x = ct_weight.keys()
# y = ct_weight.values()
# axs[0].scatter(x, y, alpha = 0.3)
# axs[0].set_yscale('log')
# axs[0].set_xscale('log')
# axs[0].set_xlabel('weight')
# axs[0].set_ylabel('frequency')
# # axs[0].legend()


sccs = nx.strongly_connected_components(g)
largest_cc = max(sccs, key=len)
print ('the biggest scc has ', len(largest_cc), 'nodes')
sccs = nx.strongly_connected_components(g)
for c in sccs:
	ct_scc[len(c)] += 1

print (ct_scc)
#
# x = ct_scc.keys()
# y = ct_scc.values()
# axs[1].scatter(x, y)
# axs[1].set_yscale('log')
# axs[1].set_xscale('log')
# axs[1].set_xlabel('size of SCC')
# axs[1].set_ylabel('frequency')
#
# print ('ct = ',ct_scc)
#
# plt.savefig('statistics_full.png', bbox_inches='tight', dpi = 300)
