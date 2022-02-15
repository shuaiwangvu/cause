import csv
from z3 import *
import random
from collections import Counter
import networkx as nx

strategy_cycle_sampling = 'S2'
num_clause_limit = 2000
timeout = 1000 * 60
edge_coverage = 1.5

o = Optimize()
o.set("timeout", timeout)
print('SMT timeout = ',timeout/1000/60, 'mins')
mode = '-w'

# this method calls the SMT solver
def obtained_edges_to_remove_using_SMT (sg):
	global num_clause_limit

	count = 0
	collect_cycles = []
	encode = {}
	if len(sg.nodes) == 2:
		[l ,r] = list(sg.nodes())
		collect_cycles.append([l,r])
		count+=1
	else:
		if strategy_cycle_sampling == 'S1':
			# strategy 1: focus on edges: each edge and their counter corresponding cycle !
			edges_to_visit = set(sg.edges())
			while (len(edges_to_visit) != 0 and count < num_clause_limit):
				(l,r) =  edges_to_visit.pop()
				c = nx.shortest_path(G = sg, source = r, target=l)
				cycle_edge_set = set()
				for i in range(len(c) -1):
					j = i+1
					if (c[i], c[j]) in edges_to_visit:
						cycle_edge_set.add((c[i], c[j]))
				collect_cycles.append(c)

				count += 1
				edges_to_visit = edges_to_visit.difference(cycle_edge_set)

		elif strategy_cycle_sampling == 'S2':
		# strategy 2: focus on nodes: obtain a random pair and each l2r , r2l
			# collect_nodes_visited_set = set()
			pct_covered = 0
			while  count < num_clause_limit and pct_covered <= edge_coverage:  #
				l = random.choice(list(sg.nodes()))
				r = random.choice(list(sg.nodes()))

				if l != r:
					l2r = nx.shortest_path(G = sg, source = l, target = r)
					r2l = nx.shortest_path(G = sg, source = r, target = l)
					# print ('l2r: ', l2r)
					# print ('r2l: ', r2l)
					c = l2r[:-1] + r2l[:-1]
					# print ('l2r2l: ',c, flush=True)
					collect_cycles.append(c)
					# collect_nodes_visited_set = collect_nodes_visited_set.union(set(c))
					pct_covered += len (c) / sg.number_of_edges()
					# print ('count = ', count , ' covers ', pct_covered)
					count += 1
	# print ('this round we have ', len(collect_cycles), 'cycles')

	o = Optimize()
	o.set("timeout", timeout)

	for (left,right) in sg.edges():
		# print (left, right)
		encode_string = '<'+str(left) + '\t' + str(right) +'>'
		# print ('encode_string: ', encode_string)
		encode[(left, right)] = Bool(str(encode_string))


	for cycle in collect_cycles:
		# print ('now encode  cycle: ', cycle )
		clause = False #
		for i in range(len(cycle)):
			j = i +1
			if j == len(cycle):
				j =0
			left = cycle[i]
			right = cycle[j]
			# encode_string = '<'+str(left) + '\t' + str(right) +'>'
			# print ('encode_string: ', encode_string)
			# if (left, right) not in encode.keys():
			# 	print (encode_string)
			# 	encode[(left, right)] = Bool(str(encode_string))

			#propositional variable
			p = encode[(left, right)]
			# append the negotiation of this propositional variable
			clause = Or(clause, Not(p))
		o.add (clause)

	# when there is no weight specified.
	for e in encode.keys():
		ecd = encode[e]
		if mode =='-u':
			o.add_soft(ecd, 1)
		elif mode == '-w':
			# w = weight_map[e]
			w = sg.edges[e]['weight']
			o.add_soft(ecd, w)
	identified_edges = []
	result = o.check()
	if result== 'unknown':
		print ('Too many!!!')
		num_clause_limit -= 20
		print ('reduce clause limit to ', num_clause_limit)
		return []
	elif result == 'unsat':
		print ('unsat')
	else:
		m = o.model()
		for arc in encode.keys():
			(left, right) = arc
			if m.evaluate(encode[arc]) == False:
				identified_edges.append(arc)

	return identified_edges


def refine_graph(h, nu_min):
	g = nx.DiGraph()
	for (n,m) in h.edges():
		w = weight= h.edges[(n,m)]['weight']
		# print (w)
		g.add_edge(n, m, weight = w)

	# refine a graph g
	# now resolve each graph (instead of SCC)
	all_removed_edges = {}

	# if nu != 0, then remove some edges accordingly
	for (n, m) in g.edges():
		if (m,n) in g.edges():
			w_n_m = g.edges[(n,m)]['weight']
			w_m_n = g.edges[(m,n)]['weight']
			nu = 0
			if w_n_m >w_m_n:
				nu  = w_n_m / w_m_n
				if nu >= nu_min:
					if (n,m) not in all_removed_edges.keys():
						all_removed_edges [(m,n)] = 'removed since nu = ' + str(nu)
			elif w_n_m < w_m_n:
				nu  = w_m_n / w_n_m
				if nu >= nu_min:
					if (n,m) not in all_removed_edges.keys():
						all_removed_edges [(n,m)] = 'removed since nu = ' + str(nu)
			else:
				nu = 1

	for (n,m) in all_removed_edges.keys():
		g.remove_edge(n,m)
	print ('remove ', len (all_removed_edges), ' edges due to nu')

	round = 1
	sccs = nx.strongly_connected_components(g)
	sccs = list(sccs)
	graphs_obtained = [g.subgraph(x).copy() for x in sccs if len(x)>1]
	sccs_size = [len(x) for x in sccs]
	# print(sccs_size)
	print ('max scc size = ', max(sccs_size))

	while len(graphs_obtained) != 0:
		# print ('this is round ', round)
		round += 1
		new_graphs_to_work_on = []
		for gs in graphs_obtained:
			# if g.number_of_nodes() > 200:
			# 	print ('working on ', len (g))
			edges_removed_by_SMT = obtained_edges_to_remove_using_SMT (gs)
			gs.remove_edges_from(edges_removed_by_SMT)
			sccs = nx.strongly_connected_components(gs)
			filter_sccs = [x for x in sccs if len(x)>1]
			for s in filter_sccs:
				# if g.number_of_nodes() > 200 and len (s) > 30:
				# 	print ('\tit was decomposed to: ', len (s))
				new_graphs_to_work_on.append(gs.subgraph(s).copy())
			# print('this subgraph removes ', len(edges_removed_by_SMT))
			for (n,m) in edges_removed_by_SMT:
				# all_removed_edges += edges_removed_by_SMT
				all_removed_edges[(n,m)] = 'removed by SMT'
		graphs_obtained = new_graphs_to_work_on

	g.remove_edges_from(all_removed_edges.keys())
	return (g, all_removed_edges)
