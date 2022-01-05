import nltk
import csv

nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
# porter=PorterStemmer()
lancaster=LancasterStemmer()
lemmatizer = WordNetLemmatizer()

#
print("rocks :", lemmatizer.lemmatize("rocking"))
print("rocks :", lancaster.stem("rocking"))
print("made :", lancaster.stem("made"))

# print("corpora :", lemmatizer.lemmatize("corpora"))
#
# # a denotes adjective in "pos"
#
# print("better :", lemmatizer.lemmatize("better", pos ="a"))
#

filename = "/Users/sw-works/Documents/causalnet+/original_causal_net/causenet-precision.tsv"

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

# def mystem (s):
#
# 	s_lem = ''
# 	if '_' in s:
# 		splited = s.split('_')
# 		strings = list(map (lancaster.stem, splited))
# 		s_lem = '_'.join(strings)
# 		# print (s, s_lem)
# 	else:
# 		s_lem = lancaster.stem(s)
# 	return s_lem

print('understanding_of_“_music : ', mylem("understanding_of_“_music"))
# print('understanding_of_“_music : ', mystem("understanding_of_“_music"))
count = 0
with open(filename,'r') as f:
	# with open( "causenet-full-without-NUL.tsv", 'w') as output:
	# writer = csv.writer(output, delimiter='\t')
	for line in f.readlines():
		count += 1
		if count %100000 == 0:
			# break
			print ('processed: ', count)
		s_lem = ''
		if '\0' in line:
			print ('row ', count,' has NUL')
			count_0 += 1
		else:
			row = line.split('\t')
			s = row[0]
			o = row[1]
			# w = int(row[2])
			s_lem = mylem(s)
			o_lem = mylem(o)
			if s != s_lem:
				print ('[slem-s]before ', s, ' after ', s_lem)
			if o != o_lem:
				print ('[slem-o]before ', o, ' after ', o_lem)

			# s_lem = mystem(s)
			# o_lem = mystem(o)
			# if s != s_lem:
			# 	print ('[stem-s]before ', s, ' after ', s_lem)
			# if o != o_lem:
			# 	print ('[stem-o]before ', o, ' after ', o_lem)
print('count = ', count)
