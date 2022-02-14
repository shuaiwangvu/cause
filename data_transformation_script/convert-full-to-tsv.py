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

# print("Started Reading JSON file")
# with open("causenet-sample.json", "r") as read_file:
# # with open("causenet-precision.jsonl", "r") as read_file:
# 	print("Converting JSON encoded data into Python dictionary")
# 	# developer = json.load(read_file)
# 	developer = [json.loads(line) for line in read_file]
#
# 	print("Decoded JSON Data From File")
# 	for key in developer:
# 		print('\ncause = ', key['causal_relation']['cause']['concept'])
# 		print('effect = ', key['causal_relation']['effect']['concept'])
# 	print("Done reading json file")

ct_sources = Counter()
ct_weight = Counter()
ct_scc = Counter()
count = 0
# with open('causenet-full.jsonl', 'r') as json_file:
with open( "causenet-full.tsv", 'w') as output:
	writer = csv.writer(output, delimiter='\t')
	with open('causenet-precision.jsonl', 'r') as json_file:
		json_list = list(json_file)
		g = nx.DiGraph()
		for json_str in json_list:
			count += 1
			print ('processing ', count)
			# if count % 1000 == 0:
			# 	# print ('Loaded: ', count)
			# 	break
			result = json.loads(json_str)
			# print(f"result: {result}")
			# print(isinstance(result, dict))
			s = result['causal_relation']['cause']['concept']
			o = result['causal_relation']['effect']['concept']
			num_sources = len(result['sources'])
			# print('#sources = weight: ', num_sources)

			g.add_edge(s, o)
			# print('\ncause = ', s)
			# print('effect = ', o)
			if '\0' not in s and '\0' not in o:
				writer.writerow([s, o, num_sources])


print ('The graph has ', g.number_of_nodes(), ' nodes')
print ('The graph has ', g.number_of_edges(), ' edges')


with open('causenet-full.tsv','r') as f:
	with open( "causenet-full-without-NUL.tsv", 'w') as output:
		writer = csv.writer(output, delimiter='\t')
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
				if '\0' not in s and '\0' not in o:
					writer.writerow([s, o, num_sources])

#
# for sc in ct_sources.keys():
# 	print ('source ', sc, ' appears ', ct_sources[sc], ' times')
# 	print ('\t\t{:6.2f}%'.format(100*ct_sources[sc] / sum(ct_sources.values())))
#
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
#
#
# sccs = nx.strongly_connected_components(g)
# largest_cc = max(sccs, key=len)
# print ('the biggest scc has ', len(largest_cc), 'nodes')
# sccs = nx.strongly_connected_components(g)
# for c in sccs:
# 	ct_scc[len(c)] += 1
#
# print (ct_scc)
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
# plt.savefig('statistics.png', bbox_inches='tight', dpi = 300)
#
# plt.show()
# # print ('these nodes are: ')
# # for n in list(largest_cc)[:10]:
# # 	print (n)
# # 	for m in g.neighbors(n):
# # 		print ('\t', m)
