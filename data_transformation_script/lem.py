# using in this file, we convert the strings to its lemmatized form
#

import json
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
import csv
import nltk
import csv
import time



nltk.download('wordnet')
nltk.download('omw-1.4')


from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.stem import PorterStemmer
# from nltk.stem import LancasterStemmer
# porter=PorterStemmer()
# lancaster=LancasterStemmer()
lemmatizer = WordNetLemmatizer()

def mylem (s):
	s_lem = ''
	if '_' in s:
		splited = s.split('_')
		strings = list(map (lemmatizer.lemmatize, splited))
		s_lem = '_'.join(strings)
		# print (s, s_lem)
	else:
		s_lem = lemmatizer.lemmatize(s)
	return s_lem

start = time.time()
ct_sources = Counter()
ct_weight = Counter()
ct_scc = Counter()
count_0 = 0
count = 0
count_lemed = 0
lem_mapping = {}
map_edge_to_sum_weight = Counter()
with open('causenet-full-without-NUL.tsv','r') as f:
	with open( "causenet-full-without-NUL-lem.tsv", 'w') as output:
		writer = csv.writer(output, delimiter='\t')
		for line in f.readlines():
			count += 1
			if count %100000 == 0:

				print ('processed: ', count)
				# break

			if '\0' in line:
				print ('row ', count,' has NUL')
				count_0 += 1
			else:
				row = line.split('\t')
				s = row[0]
				o = row[1]
				w = int(row[2])
				s_lem = mylem(s)
				o_lem = mylem(o)

				if o_lem != o:
					if o_lem  not in lem_mapping.keys():
						lem_mapping[o_lem] = set()
						lem_mapping[o_lem].add(o)
					else:
						lem_mapping[o_lem].add(o)

				if s_lem != s:
					if s_lem not in lem_mapping.keys():
						lem_mapping[s_lem] = set()
						lem_mapping[s_lem].add(s)
					else:
						lem_mapping[s_lem].add(s)

				if '\0' not in s and '\0' not in o:
					map_edge_to_sum_weight[(s_lem, o_lem)] += w
				else:
					print ('this edge contains NUL!')

		for (s_lemed, o_lemed) in map_edge_to_sum_weight.keys():
			w_lemed = map_edge_to_sum_weight[(s_lemed, o_lemed)]
			writer.writerow([s_lemed, o_lemed, w_lemed])

print ('I found ', count_0, ' lines with NUL')
print ('I found ', len(lem_mapping.keys()), 'merged nodes from ', len (lem_mapping.values()), ' original nodes')


# export this lem_mapping

with open( "lem_mapping-lem.tsv", 'w') as output:
	writer = csv.writer(output, delimiter='\t')
	writer.writerow(['Lemmatized', 'Original'])
	for k in lem_mapping.keys():
		for v in lem_mapping[k]:
			writer.writerow([k, v])



end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
time_formated = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)
print ('time taken: ' + time_formated)

# found  5574204 merged nodes from  5574204  original nodes

# print ('the new graph has X nodes and Y edges')
# print ('next, we extra common concepts from this graph')

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
