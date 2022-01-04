# this script is a small analysis of the popularity of the sources

import json
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
import csv

ct_sources = Counter()
count = 0

with open('causenet-full.jsonl', 'r') as json_file:
	json_list = list(json_file)

	for json_str in json_list:
		count += 1
		if count % 100000 == 0:
			print ('Loaded: ', count)

		result = json.loads(json_str)
		num_sources = len(result['sources'])
		# edge_to_weight[(s,o)] = num_sources
		for sc in result['sources']:
			ct_sources[sc['type']] += 1

print ('count edges = ', count)
for sc in ct_sources.keys():
	print ('source ', sc, ' appears ', ct_sources[sc], ' times')
	print ('\t\t{:6.2f}%'.format(100*ct_sources[sc] / sum(ct_sources.values())))


# the result is as follows:

# count edges =  11609890
# source  wikipedia_sentence  appears  855683  times
# 		  3.50%
# source  clueweb12_sentence  appears  23567431  times
# 		 96.42%
# source  wikipedia_list  appears  12391  times
# 		  0.05%
# source  wikipedia_infobox  appears  7916  times
# 		  0.03%
