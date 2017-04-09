#Not sure if this is particularly useful when building an initial corpus . . . but this definitely works ex post facto.
#imports Stanford’s Dependency Parser and sets up environment.

print('Before starting, the script will help you set up the paths to the Stanford dependency parser components needed to run the raw text parser. As the system is set up, it will not print out the whole sentence as part of the array. You can change this by deleting the hashtag indicating that this was a note in the corpus_callosum() module prior to running.')
print('=========')
print('')
print('This script is designed to look for keywords that can be construed as the target domain in metaphor research.')
print('=========')
print('')
print('')
from nltk.parse.stanford import StanfordDependencyParser as sparse
pathmodelsjar = input('path to the Stanford dependency language models you intend to use: ')
pathjar = input('path to the .jar for Stanford dependency parser: ')
depparse = sparse(path_to_jar=pathjar, path_to_models_jar=pathmodelsjar)

directory = '/Users/' + input('the computer user name: ') + '/Desktop/'
builderfile = directory + input('filename for csv output: ') + '.csv'

#Limits analysis to solely the dependency tree level of interest
def lmtc_pfc(ventral_stream, v2, litc_lmtc, litc_pfc, dobj):
	for tuple in ventral_stream:
		if tuple[0] == v2:
			litc_lmtc.append(tuple)
			if tuple[1] == 'dobj':
				dobj.append(tuple[2][0])
	for tuple in litc_lmtc:
		litc_pfc.append(tuple[1])

#Finds and arranges relevant oblique data
def oblique(ventral_stream, v3, met_case_marker, search):
	for tuple in ventral_stream:
		if search in tuple[2][0] and 'JJ' in tuple[2][1]:
			v3.append(tuple[2][0])
			met_case_marker.append(tuple[0][0])
		elif 'mod' in tuple[1] and search in (tuple[2][0] or tuple[0][0]):
			v3.append(tuple[2])
			for tuple in ventral_stream:
				if tuple[0] == v3[0] and tuple[1] == 'case':
					met_case_marker.append(tuple[2])
				elif search in tuple[2][0] and 'RB' in tuple[0][1]:
					met_case_marker.append(tuple[0])




#Generates the array that will be passed to KellyGEN
def corpus_callosum(corpus_callosum1, met_case_marker, adv_nmod, dobj, v1, litc_pfc, litc_lmtc, v3, sentence, TEST):
	corpus_callosum1.append(v1[0][2][0])
	corpus_callosum1.append(dobj[0]) if len(dobj) != 0 else corpus_callosum1.append('0')
	corpus_callosum1.append(str(litc_pfc).replace(',', ' '))
	corpus_callosum1.append(litc_lmtc[0][0][0])
	if len(met_case_marker) != 0:
		corpus_callosum1.append(met_case_marker[0][0])
		corpus_callosum1.append(v3[0][0])
	elif len(met_case_marker) == 0 and len(adv_nmod) == 0:
		corpus_callosum1.append(int(0))
		corpus_callosum1.append(int(0))
	#corpus_callosum1.append(sentence)
	brocas(sentence, litc_pfc, litc_lmtc, corpus_callosum1, TEST)

#Prints and sends array to relevant next steps
def brocas(sentence, litc_pfc, litc_lmtc, array, TEST='non'):
	print('==============')
	if TEST == 'non':
		print(sentence)
		print('')
	if TEST == 'test':
		print('Grammatical Structure:')
		print(litc_pfc)
		print(' ')
		print('Lexical Items:')
		print(litc_lmtc)
		print(' ')
	#Builds the training data sheet for you, if selected.
	if TEST == 'build':
		Training_Data_Builder(array)
	print('Array: ')
	print(array)
	print('==============')

def occipital(sentence, search1=None, TEST='non'):
	#Resets triggers and data failsafes
	v1 = []
	v2 = ''
	v3 = []
	met_case_marker = []
	dobj = []
	adv_nmod = []
	ventral_stream = []
	litc_lmtc = []
	litc_pfc = []
	corpus_callosum1 = []
	#components from Stanford's Dependency parser to create dep. tree.
	res = depparse.raw_parse(sentence)
	dep = res.__next__()
	ventral_stream = list(dep.triples())
	for tuple in ventral_stream:
		if tuple[1] == 'nsubj' or tuple[1] == 'nsubjpass':
			v1.append(tuple)
	if len(v1) > int(0):
		v2 = v1[0][0]
		lmtc_pfc(ventral_stream, v2, litc_lmtc, litc_pfc, dobj)
		oblique(ventral_stream, v3, met_case_marker, search1)
		corpus_callosum(corpus_callosum1, met_case_marker, adv_nmod, dobj, v1, litc_pfc, litc_lmtc, v3, sentence, TEST)
		#print(corpus_callosum1)
	elif len(v1) == 0:
		print('==============')
		print("No dependency structure to analyze")
		print(sentence)
		print('==============')

import codecs
import csv

#takes data and saves it to a CSV to build training file.
def Training_Data_Builder(array):
	with codecs.open('/Users/ZaqRosen/Desktop/Met_Training_Data.csv', 'a', 'utf-8') as csvfile:
		databuilder = csv.writer(csvfile, delimiter=',',
				quotechar='|',
				quoting=csv.QUOTE_MINIMAL)
		databuilder.writerow(array)
	csvfile.close()



#Builds the training data from a printed corpus. Designate your corpus file, the search term(s) you’re looking for, and it’ll feed each one to occipital() in build mode. 
def pvc(file, search, function='non'):
	doc = codecs.open(file, 'r', 'utf-8')
	searchlines = doc.readlines()
	doc.close()
	for i, line in enumerate(searchlines):
		for item in search:
			if item in line:
				line2 = line.replace('\\', '').replace('}', '').replace('uc0u8232', '').replace('\'92', '\'').replace('a0', '').replace('\'93', '\"').replace('\'94', '\"').replace('\'96', ',').replace('\'97', ',').replace('f0fs24 ', '').replace('cf0 ', '')
				occipital(line2, item, function)



def test(sentence):
	res = depparse.raw_parse(sentence)
	dep = res.__next__()
	ventral_stream = list(dep.triples())
	for tuple in ventral_stream:
		print(tuple)
