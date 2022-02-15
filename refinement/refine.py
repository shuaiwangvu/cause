
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
from refine_to_dag import refine_graph

ct_weighted_degree = Counter()
ct_weight = Counter()

edge_to_weight = {}

g = nx.DiGraph()
count = 0
filename_causenet_tsv = './core-raw.tsv'

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


#
# centrality = nx.katz_centrality(g, weight='weight')
centrality = nx.eigenvector_centrality(g, weight='weight')
s = {k: v for k, v in sorted(centrality.items(), key=lambda item: item[1], reverse=True)}

core = nx.DiGraph()

count = 0
for k in s:

	count += 1
	if centrality[k] >= 0.0001:
		print (k)
		print ('\thas centrality     : ',s[k])
		print ('\thas degree         : ',g.degree(k))
		print ('\thas weighted degree: ',g.degree(k, weight='weight'))
		core.add_node(k)

core = g.subgraph(core.nodes())
print ('the core graph has ', core.number_of_nodes(), ' nodes')
print ('the core graph has ', core.number_of_edges(), ' edges')

sccs = nx.strongly_connected_components(core)
largest_cc = max(sccs, key=len)
print ('the biggest scc has ', len(largest_cc), 'nodes')

core_raw = open ("core-raw.tsv", "w")
core_raw.write('Source\tTarget\tWeight_Source_Target\tAnnotation\n')

# export the graph
for (s,t) in core.edges():
	weight = core[s][t]['weight']
	# print ('weight = ', weight)
	w_s_t = edge_to_weight [(s,t)]
	core_raw.write(str(s)+'\t'+ str(t) +'\t'+ str(w_s_t)+ '\tTBD\n')


core_refined, removed_edges_with_reason = refine_graph(core_raw, nu = 20)

core_refined = open ("core-refined.tsv", "w")
core_refined.write('Source\tTarget\tWeight_Source_Target\tAnnotation\n')

core_removed_in_refinement = open ("core-removed-in-refinement.tsv", "w")
core_removed_in_refinement.write('Source\tTarget\tWeight_Source_Target\tComment\n')
