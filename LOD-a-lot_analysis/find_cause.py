

from hdt import HDTDocument, IdentifierPosition
import networkx as nx
import csv

from collections import Counter

l=["http://www.co-ode.org/Biomedical-tutorial/Biomedical-TutorialTop.owl#causes",
"http://dbpedia.org/ontology/deathCause",
"http://iridl.ldeo.columbia.edu/ontologies/iriterms.owl#directlyImplies",
"http://iridl.ldeo.columbia.edu/ontologies/iriterms.owl#implies"]

owl_equivalentProperty = "http://www.w3.org/2002/07/owl#equivalentProperty"
subPropertyOf = 'http://www.w3.org/2000/01/rdf-schema#subPropertyOf'

PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
hdt = HDTDocument(PATH_LOD)

g = nx.MultiDiGraph()
relation_to_keyword = {}
relation_to_numtriple = {}
keyword_to_relation = {}

keywords = ['cause', 'Cause', 'causes', 'Causes', 'causal relation','Causal relation',
 'affects','Affects', 'regulates', 'Regulates', 'Impacts', 'impacts',
'induce', 'induces','Induce','Induces', 'produces', 'Produces', 'produce', 'Produces']

xmls = "^^<http://www.w3.org/2001/XMLSchema#string>"
for w in keywords:
	triples, cardinality = hdt.search_triples("", "", '"'+ w + '"'+xmls)
	print('word = ', w, ' : ', cardinality)
	for (s,p,o) in triples:
		g.add_node(s)
		relation_to_keyword[s] = w
		if w in keyword_to_relation.keys():
			keyword_to_relation[w].append(s)
		else:
			keyword_to_relation[w] = [s]

size = 0

g.add_node("http://purl.obolibrary.org/obo/RO_0004048")
g.add_node("http://purl.obolibrary.org/obo/RO_0002212")
g.add_node("http://purl.obolibrary.org/obo/ro/docs/causal-relations")
while size != g.nodes():
	size = g.nodes()
	h = nx.MultiDiGraph()
	for n in g.nodes():
		# find its inverse
		triples, _ = hdt.search_triples(n, owl_equivalentProperty, "")
		for _, _, m in triples:
			if m not in g.nodes():
				h.add_node(str(m), type = 'Extended', comment = 'inverse of '+ n)
				h.add_edge(str(n), str(m), rel='inverseOf')

		triples, _ = hdt.search_triples("", owl_equivalentProperty, n)
		for m, _, _ in triples:
			if m not in g.nodes():
				h.add_node(str(m), type = 'Extended', comment = 'inverse of '+ n)
				h.add_edge(str(m), str(n), rel='inverseOf')

		# find its subPropertyOf
		triples, _ = hdt.search_triples("", subPropertyOf, n)
		for m, _, _ in triples:
			if m not in g.nodes():
				h.add_node(str(m), type = 'Extended', comment = 'subProperty of '+ n)
				h.add_edge(str(m), str(n), rel='subPropertyOf')
	g = nx.compose(g, h)

count = 0
print ('\n\nthere are in total ', len (g.nodes()), ' causal relations collected')
for n in g.nodes():
	s_triples, s_cardinality = hdt.search_triples("", n, "")
	relation_to_numtriple[n] = s_cardinality
	count +=  s_cardinality
	keyword_to_relation['extra'] = []
	if n in relation_to_keyword.keys():
		if s_cardinality !=0:
			print ('[', relation_to_keyword[n],'] ', n, ' --> ', s_cardinality)

	else:
		print ('[extra] ', n, ' --> ', s_cardinality)
		keyword_to_relation['extra'].append(n)

print ('=======')
for w in keyword_to_relation.keys():
	print (w, '->', len(keyword_to_relation[w]))
print ('=======')
print ('there are in total ', len (relation_to_keyword.keys()), ' relations found')
print ('there are in total ', count, ' triples')
