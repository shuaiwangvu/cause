
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
		c = c.replace('’', '\'')
		e = e.replace('’', '\'')
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
		# print (k)
		# print ('\thas centrality     : ',s[k])
		# print ('\thas degree         : ',g.degree(k))
		# print ('\thas weighted degree: ',g.degree(k, weight='weight'))
		core.add_node(k)

core = g.subgraph(core.nodes()).copy()
for (n,m) in core.edges():
	# print (g.edges[(n,m)]['weight'])
	core.edges[(n,m)]['weight'] = g.edges[(n,m)]['weight']

print ('the core graph has ', core.number_of_nodes(), ' nodes')
print ('the core graph has ', core.number_of_edges(), ' edges')

sccs = nx.strongly_connected_components(core)
largest_cc = max(sccs, key=len)
print ('the biggest scc has ', len(largest_cc), 'nodes')

writer_core_raw = open ("core-raw.tsv", "w")
writer_core_raw.write('Source\tTarget\tWeight_Source_Target\tAnnotation\n')

# export the graph
for (s,t) in core.edges():
	weight = core[s][t]['weight']

	# print ('weight = ', weight)
	w_s_t = edge_to_weight [(s,t)]
	writer_core_raw.write(str(s)+'\t'+ str(t) +'\t'+ str(w_s_t)+ '\tTBD\n')

start = time.time()

reflexive_edges = []
for (n,m) in core.edges():
	if n == m:
		reflexive_edges.append((n,m))

core.remove_edges_from(reflexive_edges)
print('removed ', len(reflexive_edges), ' reflexive_edges')

new_core, removed_edges_with_reason = refine_graph(core, nu_min = 20)

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("Time taken: {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))


print ('total edges to remove: ', len (removed_edges_with_reason.keys()))

writer_core_refined = open ("core-refined.tsv", "w")
writer_core_refined.write('Source\tTarget\tWeight_Source_Target\tComment\n')

for (s, t) in new_core.edges():
	# reason = removed_edges_with_reason[(s,t)]
	# core_removed_in_refinement.write(str(s)+'\t'+str(t)+'\t'+reason+'\n')
	w_s_t = edge_to_weight [(s,t)]
	writer_core_refined.write(str(s)+'\t'+ str(t) +'\t'+ str(w_s_t)+ '\tTBD\n')

print ('the resulting graph has ', new_core.number_of_edges(), ' edges')
print ('the resulting graph has ', new_core.number_of_nodes(), ' nodes')
if (nx.algorithms.dag.is_directed_acyclic_graph(new_core)):
	print ('it is a DAG.')
else:
	print ('Mission failed: it is not a DAG.')


core_removed_in_refinement = open ("core-removed-in-refinement.tsv", "w")
core_removed_in_refinement.write('Source\tTarget\tComment\n')

for (s, t) in reflexive_edges:
	core_removed_in_refinement.write(str(s)+'\t'+str(t)+'\t'+'reflxive edge'+'\n')

for (s, t) in removed_edges_with_reason:
	reason = removed_edges_with_reason[(s,t)]
	core_removed_in_refinement.write(str(s)+'\t'+str(t)+'\t'+reason+'\n')
print ('the resulting graph has ', len (removed_edges_with_reason.keys()), ' edges removed')
