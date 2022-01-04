
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
filename_causenet_tsv = 'causenet-full-without-NUL.tsv'

with open(filename_causenet_tsv,'r') as f:
	for line in f.readlines():
		count += 1
		if count %100000 == 0:
			# break
			print ('processed: ', count)

		if '\0' in line:
			print ('row ', count,' has NUL')
			count_0 += 1
		else:
			row = line.split('\t')
			s = row[0]
			o = row[1]
			w = int(row[2])
			g.add_edge(s, o)
			ct_weight[w] += 1

print ('count_0 = ', count_0)
print ('The graph has ', g.number_of_nodes(), ' nodes')
print ('The graph has ', g.number_of_edges(), ' edges')

sccs = nx.strongly_connected_components(g)
largest_cc = max(sccs, key=len)
print ('the biggest scc has ', len(largest_cc), 'nodes')
sccs = nx.strongly_connected_components(g)
for c in sccs:
	ct_scc[len(c)] += 1

print (ct_scc)
