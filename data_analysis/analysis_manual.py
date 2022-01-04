# a small script for the analysis of cycles involving two nodes
import csv
# The two files are
file_ge3 = 'pairs_GE3_annotated100.tsv'
file_3_1 = 'pairs_3_1_annotated100.tsv'

print('==========================[GE3]=============================')
ge3_file = open(file_ge3, 'r')
reader = csv.DictReader(ge3_file, delimiter='\t')

count_right = 0
count_left = 0
count_unrelated = 0
count_unknown = 0

count_annotated = 0

for row in reader:
	s = row["Source"]
	t = row["Target"]
	w_s_t = row["Weight_Source_Target"]
	w_t_s = row["Weight_Target_Source"]
	a = row["Annotation"]
	if a != 'TBD':
		count_annotated += 1
	if a == 'right':
		count_right += 1
	elif a == 'left':
		count_left += 1
	elif  a == 'unknown':
		count_unknown += 1
	elif  a == 'unrelated':
		count_unrelated += 1
	else:
		pass

print ('total annotated = ', count_annotated)
print ('count_right = ', count_right, '{:6.2f}%'.format(100*count_right/count_annotated))
print ('count_left = ', count_left, '{:6.2f}%'.format(100*count_left/count_annotated))
print ('count_unrelated = ', count_unrelated, '{:6.2f}%'.format(100*count_unrelated/count_annotated))
print ('count_unknown = ', count_unknown, '{:6.2f}%'.format(100*count_unknown/count_annotated))

print('===========================[1 - 3]============================')

ge13_file = open(file_3_1, 'r')
reader = csv.DictReader(ge13_file, delimiter='\t')

count_right = 0
count_left = 0
count_unknown = 0
count_annotated = 0

for row in reader:
	s = row["Source"]
	t = row["Target"]
	w_s_t = row["Weight_Source_Target"]
	w_t_s = row["Weight_Target_Source"]
	a = row["Annotation"]
	if a != 'TBD':
		count_annotated += 1
	if a == 'right':
		count_right += 1
	elif a == 'left':
		count_left += 1
	elif  a == 'unknown':
		count_unknown += 1
	elif  a == 'unrelated':
		count_unrelated += 1
	else:
		pass

print ('total annotated = ', count_annotated)
print ('count_right = ', count_right, '{:6.2f}%'.format(100*count_right/count_annotated))
print ('count_left = ', count_left, '{:6.2f}%'.format(100*count_left/count_annotated))
print ('count_unrelated = ', count_unrelated, '{:6.2f}%'.format(100*count_unrelated/count_annotated))
print ('count_unknown = ', count_unknown, '{:6.2f}%'.format(100*count_unknown/count_annotated))
