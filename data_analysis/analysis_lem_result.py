
# This script perform an analysis of the degree and weights
#

import json
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
import csv
import nltk
import csv
import time


ct_weighted_degree = Counter()
ct_weight = Counter()

edge_to_weight = {}

g = nx.DiGraph()
count = 0
filename_causenet_tsv = '../../data/causenet-precision-without-NUL-lem.tsv'

# count_reflexive = 0

with open(filename_causenet_tsv, newline='') as csvfile:
	reader = csv.DictReader(csvfile, delimiter='\t')
	for row in reader:
		count += 1
		if count %1000000 == 0:
			print ('# lines read = ', count)
			# break
		c = row['Cause']
		e = row['Effect']
		w = int (row['Weight'])
		edge_to_weight[(c,e)] = w
		ct_weight[w] += 1
		g.add_edge(c, e, weight=w)

h = nx.Graph(g)
for n in h.nodes:
	degree = 0
	for m in h.neighbors(n):
		if (n,m) in edge_to_weight.keys():
			degree += edge_to_weight[(n, m)]
		elif (m,n) in edge_to_weight.keys():
			degree += edge_to_weight[(m, n)]
	ct_weighted_degree[degree] += 1

print ('# lines read = ', count)
# plot the degree
# print ('weighted_degree: ', ct_weighted_degree)
print ('weighted_degree 1: ', ct_weighted_degree[1], 'pct', ct_weighted_degree[1]/sum(ct_weighted_degree.values()))
print ('weighted_degree 2: ', ct_weighted_degree[2], 'pct', ct_weighted_degree[2]/sum(ct_weighted_degree.values()))
# print ('weight: ', ct_weight)
print ('weight 1: ', ct_weight[1], ' pct ', ct_weight[1]/sum(ct_weight.values()))
print ('weight 2: ', ct_weight[2], ' pct ', ct_weight[2]/sum(ct_weight.values()))


fig, axs = plt.subplots(2)
# axs[0].set_title('in-degree')
# axs[1].set_title('out-degree')
fig.set_figwidth(6)
fig.set_figheight(8)

axs[0].spines['top'].set_visible(False)
axs[0].spines['right'].set_visible(False)
axs[0].autoscale(tight=True)

x = ct_weighted_degree.keys()
y = ct_weighted_degree.values()
# axs[0].scatter(x, y, alpha = 0.3)
axs[0].bar(x,y)
axs[0].set_yscale('log')
axs[0].set_xscale('log')
axs[0].set_xlabel('weighted degree of nodes')
axs[0].set_ylabel('frequency')

x = ct_weight.keys()
y = ct_weight.values()

# axs[0].scatter(x, y, alpha = 0.3)
# axs[1].set_xscale('log')
axs[1].bar(x,y)
axs[1].set_yscale('log')
axs[1].set_xscale('log')
axs[1].set_xlabel('weight on edges')
axs[1].set_ylabel('frequency')
# plt.show()
plt.savefig('degree_and_edge_weights_statistics.png', bbox_inches='tight', dpi = 300)

#
# centrality = nx.katz_centrality(g, weight='weight')
centrality = nx.eigenvector_centrality(g, weight='weight')
s = {k: v for k, v in sorted(centrality.items(), key=lambda item: item[1], reverse=True)}

core = nx.DiGraph()

count = 0
for k in s:
	print (k)
	print ('\thas centrality     : ',s[k])
	print ('\thas degree         : ',g.degree(k))
	print ('\thas weighted degree: ',g.degree(k, weight='weight'))
	count += 1
	core.add_node(k)
	if count >= 5000:
		break

core = g.subgraph(core.nodes())
print ('the core graph has ', core.number_of_nodes(), ' nodes')
print ('the core graph has ', core.number_of_edges(), ' edges')

sccs = nx.strongly_connected_components(core)
largest_cc = max(sccs, key=len)
print ('the biggest scc has ', len(largest_cc), 'nodes')
