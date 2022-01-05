# this file is about an analysis of the degree of the CauseNet
# we plot the result and export it.
#

import json
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
import csv
import codecs
import math



g = nx.DiGraph()
count_0 = 0
count = 0
weight_proportion = []
# filename_causenet_tsv = 'causenet-full-without-NUL.tsv'
filename_causenet_tsv = 'causenet-full-without-NUL-lem.tsv'
#
with open(filename_causenet_tsv,'r') as f:
	for line in f.readlines():
		count += 1
		if count %1000000 == 0:
			# break
			print ('processed: ', count)

		if '\0' in line:
			print ('row ', count,' has NUL')
			count_0 += 1
		else:
			row = line.split('\t')
			s = row[0]
			o = row[1]
			# w = int(row[2])
			# edge_to_weight[(s,o)] = w
			if s!=o:
				g.add_edge(s, o)


print ('count_0 = ', count_0)
print ('The graph has ', g.number_of_nodes(), ' nodes')
print ('The graph has ', g.number_of_edges(), ' edges')

print ('-------------DEGREE-------------')
max_out_sorted = list(g.nodes())
max_out_sorted.sort(key=g.out_degree, reverse = True)
for m in max_out_sorted[:50]:
	print ('node = ', m, ' out-degree ', g.out_degree(m), ' in-degree ', g.in_degree(m))
print ('\n')
max_in_sorted = list(g.nodes())
max_in_sorted.sort(key=g.in_degree, reverse = True)
for m in max_in_sorted[:50]:
	print ('node = ', m, ' in-degree ', g.in_degree(m), ' out-degree ', g.out_degree(m))

print ('death neighbors: ', list(g.neighbors('death'))[:50])
print ('stress neighbors: ', list(g.neighbors('stress'))[:50])

# before Lem:
# ============================================================
# The graph has  12186021  nodes
# The graph has  11606999  edges
# -------------DEGREE-------------
# node =  events  out-degree  13346  in-degree  2820
# node =  disease  out-degree  11742  in-degree  15887
# node =  stress  out-degree  10352  in-degree  9276
# node =  changes  out-degree  9680  in-degree  9856
# node =  conditions  out-degree  8741  in-degree  4317
# node =  problems  out-degree  8412  in-degree  66214
# node =  condition  out-degree  7729  in-degree  6663
# node =  injury  out-degree  7401  in-degree  15109
# node =  war  out-degree  7255  in-degree  5266
# node =  infection  out-degree  7254  in-degree  6545
# node =  actions  out-degree  6919  in-degree  1922
# node =  work  out-degree  6905  in-degree  1160
# node =  accident  out-degree  6525  in-degree  8077
# node =  failure_to_do_so  out-degree  6471  in-degree  42
# node =  change  out-degree  6195  in-degree  5575
# node =  incident  out-degree  6080  in-degree  1840
# node =  climate_change  out-degree  5877  in-degree  1884
# node =  depression  out-degree  5616  in-degree  10818
# node =  smoking  out-degree  5466  in-degree  582
# node =  action  out-degree  5387  in-degree  2824
# node =  bacteria  out-degree  5158  in-degree  1222
# node =  death  out-degree  5085  in-degree  46723
# node =  drugs  out-degree  5047  in-degree  684
# node =  global_warming  out-degree  5017  in-degree  3048
# node =  virus  out-degree  4881  in-degree  368
# node =  illness  out-degree  4827  in-degree  7740
# node =  god  out-degree  4628  in-degree  610
# node =  obesity  out-degree  4455  in-degree  4418
# node =  fire  out-degree  4361  in-degree  4854
# node =  diseases  out-degree  4349  in-degree  9003
# node =  diabetes  out-degree  4337  in-degree  3186
# node =  inflammation  out-degree  4254  in-degree  6731
# node =  alcohol  out-degree  4183  in-degree  440
# node =  damage  out-degree  4159  in-degree  29638
# node =  cancer  out-degree  4004  in-degree  10453
# node =  aging  out-degree  4002  in-degree  1312
# node =  trauma  out-degree  3934  in-degree  2018
# node =  success  out-degree  3924  in-degree  11687
# node =  drug  out-degree  3903  in-degree  333
# node =  injuries  out-degree  3876  in-degree  11942
# node =  efforts  out-degree  3797  in-degree  105
# node =  situation  out-degree  3772  in-degree  3518
# node =  exposure  out-degree  3743  in-degree  976
# node =  pain  out-degree  3731  in-degree  23519
# node =  failure  out-degree  3692  in-degree  7707
# node =  mutations  out-degree  3550  in-degree  1569
# node =  anxiety  out-degree  3539  in-degree  7399
# node =  earthquake  out-degree  3470  in-degree  696
# node =  mutation  out-degree  3413  in-degree  698
# node =  activities  out-degree  3386  in-degree  903
#
#
# node =  problems  in-degree  66214  out-degree  8412
# node =  death  in-degree  46723  out-degree  5085
# node =  damage  in-degree  29638  out-degree  4159
# node =  pain  in-degree  23519  out-degree  3731
# node =  problem  in-degree  16229  out-degree  2681
# node =  disease  in-degree  15887  out-degree  11742
# node =  increase  in-degree  15473  out-degree  1933
# node =  injury  in-degree  15109  out-degree  7401
# node =  symptoms  in-degree  14875  out-degree  2792
# node =  confusion  in-degree  14475  out-degree  2225
# node =  costs  in-degree  14472  out-degree  946
# node =  deaths  in-degree  13357  out-degree  1057
# node =  injuries  in-degree  11942  out-degree  3876
# node =  success  in-degree  11687  out-degree  3924
# node =  depression  in-degree  10818  out-degree  5616
# node =  cancer  in-degree  10453  out-degree  4004
# node =  harm  in-degree  9952  out-degree  323
# node =  changes  in-degree  9856  out-degree  9680
# node =  stress  in-degree  9276  out-degree  10352
# node =  diseases  in-degree  9003  out-degree  4349
# node =  trouble  in-degree  8144  out-degree  267
# node =  losses  in-degree  8130  out-degree  1001
# node =  accident  in-degree  8077  out-degree  6525
# node =  loss  in-degree  7859  out-degree  2388
# node =  illness  in-degree  7740  out-degree  4827
# node =  complications  in-degree  7718  out-degree  2004
# node =  failure  in-degree  7707  out-degree  3692
# node =  anxiety  in-degree  7399  out-degree  3539
# node =  violence  in-degree  7164  out-degree  2772
# node =  destruction  in-degree  7114  out-degree  985
# node =  side_effects  in-degree  7095  out-degree  1407
# node =  damages  in-degree  7080  out-degree  456
# node =  delays  in-degree  6988  out-degree  1545
# node =  inflammation  in-degree  6731  out-degree  4254
# node =  condition  in-degree  6663  out-degree  7729
# node =  health_problems  in-degree  6662  out-degree  791
# node =  infection  in-degree  6545  out-degree  7254
# node =  discomfort  in-degree  6272  out-degree  576
# node =  difficulties  in-degree  6194  out-degree  942
# node =  delay  in-degree  5963  out-degree  2186
# node =  headaches  in-degree  5926  out-degree  427
# node =  decline  in-degree  5846  out-degree  683
# node =  change  in-degree  5575  out-degree  6195
# node =  growth  in-degree  5565  out-degree  2415
# node =  suffering  in-degree  5546  out-degree  518
# node =  accidents  in-degree  5472  out-degree  3014
# node =  decrease  in-degree  5409  out-degree  494
# node =  vulnerabilities  in-degree  5274  out-degree  210
# node =  war  in-degree  5266  out-degree  7255
# node =  mortality  in-degree  5236  out-degree  570
# death neighbors:  ['grief', 'pain', 'loss', 'sadness', 'life', 'depression', 'losses', 'sorrow', 'financial_loss', 'suffering', 'rebirth', 'problems', 'resurrection', 'anger', 'damages', 'injury', 'vacancy', 'confusion', 'sin', 'separation', 'termination', 'protests', 'illness', 'public_outcry', 'by-election', 'damage', 'problem', 'vacancies', 'shock', 'blindness', 'peace', 'new_life', 'stress', 'great_sorrow', 'disease', 'anguish', 'feelings', 'events', 'war', 'violence', 'outpouring_of_grief', 'anxiety', 'civil_war', 'general_regret', 'fear', 'widespread_sorrow', 'outcry', 'issues', 'accident', 'change']
# stress neighbors:  ['illness', 'depression', 'insomnia', 'health_problems', 'disease', 'headaches', 'problems', 'hair_loss', 'weight_gain', 'fatigue', 'pain', 'death', 'ulcers', 'symptoms', 'high_blood_pressure', 'diseases', 'anxiety', 'acne', 'condition', 'physical_symptoms', 'headache', 'illnesses', 'heart_attack', 'cancer', 'problem', 'burnout', 'diabetes', 'ibs', 'conditions', 'migraine', 'impotence', 'hypertension', 'heart_attacks', 'stomach_ulcers', 'migraines', 'mental_illness', 'heart_disease', 'sleeplessness', 'infertility', 'back_pain', 'damage', 'anger', 'muscle_tension', 'obesity', 'erectile_dysfunction', 'tension', 'injury', 'sickness', 'panic_attacks', 'miscarriage']




# after Lem:
# ============================================================
# The graph has  11881187  nodes
# The graph has  11499012  edges
# -------------DEGREE-------------
# node =  change  out-degree  15310  in-degree  14708
# node =  event  out-degree  15190  in-degree  3598
# node =  condition  out-degree  15160  in-degree  10165
# node =  disease  out-degree  14726  in-degree  22667
# node =  action  out-degree  11737  in-degree  4509
# node =  stress  out-degree  10568  in-degree  9931
# node =  problem  out-degree  10535  in-degree  78481
# node =  injury  out-degree  10368  in-degree  24365
# node =  infection  out-degree  9004  in-degree  10105
# node =  accident  out-degree  8757  in-degree  12665
# node =  war  out-degree  8062  in-degree  6454
# node =  drug  out-degree  7972  in-degree  977
# node =  incident  out-degree  7668  in-degree  2841
# node =  work  out-degree  7138  in-degree  1501
# node =  virus  out-degree  6856  in-degree  715
# node =  mutation  out-degree  6549  in-degree  2140
# node =  failure_to_do_so  out-degree  6369  in-degree  43
# node =  climate_change  out-degree  5971  in-degree  2026
# node =  death  out-degree  5891  in-degree  55388
# node =  activity  out-degree  5797  in-degree  1797
# node =  illness  out-degree  5604  in-degree  9957
# node =  depression  out-degree  5568  in-degree  10769
# node =  fire  out-degree  5317  in-degree  6448
# node =  smoking  out-degree  5278  in-degree  569
# node =  situation  out-degree  5049  in-degree  4270
# node =  effort  out-degree  4927  in-degree  303
# node =  bacteria  out-degree  4914  in-degree  1201
# node =  global_warming  out-degree  4842  in-degree  2950
# node =  attack  out-degree  4810  in-degree  2469
# node =  error  out-degree  4735  in-degree  8732
# node =  god  out-degree  4655  in-degree  651
# node =  storm  out-degree  4644  in-degree  935
# node =  failure  out-degree  4617  in-degree  9386
# node =  earthquake  out-degree  4554  in-degree  2075
# node =  damage  out-degree  4465  in-degree  34215
# node =  obesity  out-degree  4323  in-degree  4303
# node =  cancer  out-degree  4272  in-degree  11562
# node =  conflict  out-degree  4265  in-degree  6439
# node =  medication  out-degree  4247  in-degree  327
# node =  success  out-degree  4204  in-degree  12126
# node =  diabetes  out-degree  4196  in-degree  3110
# node =  inflammation  out-degree  4170  in-degree  6602
# node =  disorder  out-degree  4114  in-degree  4875
# node =  alcohol  out-degree  4072  in-degree  441
# node =  exposure  out-degree  4035  in-degree  1191
# node =  trauma  out-degree  3958  in-degree  2095
# node =  behavior  out-degree  3937  in-degree  3386
# node =  aging  out-degree  3907  in-degree  1295
# node =  development  out-degree  3783  in-degree  2249
# node =  pain  out-degree  3745  in-degree  23228
#
#
# node =  problem  in-degree  78481  out-degree  10535
# node =  death  in-degree  55388  out-degree  5891
# node =  damage  in-degree  34215  out-degree  4465
# node =  injury  in-degree  24365  out-degree  10368
# node =  pain  in-degree  23228  out-degree  3745
# node =  disease  in-degree  22667  out-degree  14726
# node =  increase  in-degree  17334  out-degree  2418
# node =  cost  in-degree  15725  out-degree  1304
# node =  loss  in-degree  14852  out-degree  3270
# node =  change  in-degree  14708  out-degree  15310
# node =  symptom  in-degree  14586  out-degree  2785
# node =  confusion  in-degree  14362  out-degree  2220
# node =  accident  in-degree  12665  out-degree  8757
# node =  delay  in-degree  12281  out-degree  3548
# node =  success  in-degree  12126  out-degree  4204
# node =  cancer  in-degree  11562  out-degree  4272
# node =  depression  in-degree  10769  out-degree  5568
# node =  harm  in-degree  10492  out-degree  347
# node =  condition  in-degree  10165  out-degree  15160
# node =  infection  in-degree  10105  out-degree  9004
# node =  illness  in-degree  9957  out-degree  5604
# node =  stress  in-degree  9931  out-degree  10568
# node =  failure  in-degree  9386  out-degree  4617
# node =  trouble  in-degree  9248  out-degree  531
# node =  error  in-degree  8732  out-degree  4735
# node =  headache  in-degree  7918  out-degree  709
# node =  complication  in-degree  7917  out-degree  2219
# node =  difficulty  in-degree  7575  out-degree  1148
# node =  anxiety  in-degree  7477  out-degree  3532
# node =  side_effect  in-degree  7109  out-degree  1494
# node =  violence  in-degree  7017  out-degree  2710
# node =  destruction  in-degree  7001  out-degree  981
# node =  health_problem  in-degree  6603  out-degree  873
# node =  inflammation  in-degree  6602  out-degree  4170
# node =  war  in-degree  6454  out-degree  8062
# node =  fire  in-degree  6448  out-degree  5317
# node =  conflict  in-degree  6439  out-degree  4265
# node =  decline  in-degree  6406  out-degree  818
# node =  discomfort  in-degree  6282  out-degree  606
# node =  vulnerability  in-degree  6251  out-degree  622
# node =  disaster  in-degree  5871  out-degree  2289
# node =  decrease  in-degree  5825  out-degree  571
# node =  suffering  in-degree  5678  out-degree  578
# node =  growth  in-degree  5578  out-degree  2461
# node =  crisis  in-degree  5244  out-degree  3003
# node =  mortality  in-degree  5207  out-degree  575
# node =  controversy  in-degree  5160  out-degree  1656
# node =  fatigue  in-degree  5071  out-degree  1850
# node =  disorder  in-degree  4875  out-degree  4114
# node =  issue  in-degree  4872  out-degree  2217
# death neighbors:  ['grief', 'pain', 'loss', 'sadness', 'life', 'depression', 'sorrow', 'financial_loss', 'suffering', 'rebirth', 'problem', 'resurrection', 'anger', 'damage', 'injury', 'vacancy', 'confusion', 'sin', 'separation', 'termination', 'protest', 'illness', 'public_outcry', 'by-election', 'shock', 'blindness', 'peace', 'new_life', 'stress', 'great_sorrow', 'disease', 'anguish', 'feeling', 'event', 'war', 'violence', 'outpouring_of_grief', 'anxiety', 'civil_war', 'general_regret', 'fear', 'widespread_sorrow', 'outcry', 'issue', 'accident', 'change', 'birth', 'complication', 'bleeding', 'succession_crisis']
# stress neighbors:  ['illness', 'depression', 'insomnia', 'health_problem', 'disease', 'headache', 'problem', 'hair_loss', 'weight_gain', 'fatigue', 'pain', 'death', 'ulcer', 'symptom', 'high_blood_pressure', 'anxiety', 'acne', 'condition', 'physical_symptom', 'heart_attack', 'cancer', 'burnout', 'diabetes', 'ibs', 'migraine', 'impotence', 'hypertension', 'stomach_ulcer', 'mental_illness', 'heart_disease', 'sleeplessness', 'infertility', 'back_pain', 'damage', 'anger', 'muscle_tension', 'obesity', 'erectile_dysfunction', 'tension', 'injury', 'sickness', 'panic_attack', 'miscarriage', 'change', 'tension_headache', 'heart_problem', 'physical_illness', 'constipation', 'disorder', 'overeating']
