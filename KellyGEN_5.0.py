#Problem with litc such that it's not returning a value to corpus callosum . . .
# or anywhere, really. System currently breaks during oblique() in corpus
# Callosum, which means the conditions for the for gate preceding packaging
# are never met--v3 is ALWAYS an empty list. Tried fixing (current iteration).
# Information is not getting passed and stored in corpus_callosum. The question
# is . . . why???

#imports Stanford’s Dependency Parser and sets up environment.
from nltk.parse.stanford import StanfordDependencyParser as sparse
pathmodelsjar = '/Users/ZaqRosen/nltk_data/stanford-english-corenlp-2016-01-10-models.jar'
pathjar = '/Users/ZaqRosen/nltk_data/stanford-parser/stanford-parser.jar'
depparse = sparse(path_to_jar=pathjar, path_to_models_jar=pathmodelsjar)

#Update progress note:
print('Start from idea for the corpus all for media_type.start()')

#
##
##Dependency to Constructions pipeline {Using Stanford's Dependency Parser}##
##
#
#This will be autodefined to 'nsubj' or 'dobj', but the point is to find
# any local deps that correlate to the sentence headers, essentially--those
# bits that more or less establish the relationship of the verb. The POS#
# .append protocol is effectively a fail-safe in case you end up analyzing
# a sub-structure lacking the 'nsubj' and 'dobj' components.
def litc(POS1, POS2, listy):
	for tuple in listy:
		POS1.append(tuple[2][0]) if 'nsubj' in tuple[1] else 0
		POS2.append(tuple[2][0]) if 'dobj' in tuple[1] else 0
	POS1.append('0')
	POS2.append('0')

#We know that WHAT the dep tree looks like is important--is it just an ADJ.P?
# or is the search item part of the entire clausal unit? This'll get to the
# bottom of these questions.
def sylvan(lmtc, pfc):
	for tuple in lmtc:
		pfc.append(tuple[1])

#Oblique elements appear to be vitally important in metaphor and constructional
# analyses. This block will thus derive the oblique elements' structure in
# simplified terms, or establish an adjective relationship of some sort to
# analyze.
def obl(oblique, lmtc, ventral_stream):
	oblique.append((0,0))
	for tuple in lmtc:
		oblique.append((tuple[2][0], tuple[0][0])) if 'JJ' in tuple[2][1] else 0
		if 'mod' in tuple[1]:
			ph_head = tuple[2]
			for tuple in ventral_stream:
				oblique.append((tuple[2][0], ph_head[0])) if tuple[1]=='case' and tuple[0]==ph_head else 0

def print_protocol( a, b, c, d):
	e = [a, b, c, d]
	for item in e:
		print('')
		print(item)
		print('=========')
			
#Where the magic happens, this links everything up into a coherent chunk that
# can then be passed to another function later in order to utilize the const.
# components, or print everything to a .csv via brocas().
def corpus_callosum(ventral_stream, v1, lmtc, sentence, media, TEST):
	oblique=[]
	pfc=[]
	NSUBJ=[]
	DOBJ=[]
	sylvan(lmtc, pfc)
	litc(NSUBJ, DOBJ, lmtc)
	obl(oblique, lmtc, ventral_stream)
	#print_protocol(oblique, pfc, NSUBJ, DOBJ)
	for item in oblique:
		corpus_callosum1 = [media,
			NSUBJ[0], DOBJ[0], pfc, v1[0], item[0], item[1],
			sentence
			]
		brocas(sentence, pfc, lmtc, corpus_callosum1, TEST)
		corpus_callosum1 = []
		
#This little function simply packages and presents all the data collected in
# an easily interpretable chunk. If TEST=='build', it'll generate a .csv of
# the data the rest of the script collects.
def brocas(sentence, pfc, lmtc, array, TEST='non'):
	print('==============')
	if TEST == 'non':
		print(sentence)
		print('')
	if TEST == 'test':
		print('Grammatical Structure:')
		print(pfc)
		print(' ')
		print('Lexical Items:')
		print(lmtc)
		print(' ')
	#Builds the training data sheet for you, if selected.
	if TEST == 'build':
		Training_Data_Builder(array)
	print('Array: ')
	print(array)
	print('==============')

#Occipital(), named after the occipital lobe, is the integrative tissue
# that triggers the whole process, and links all the components together.
def occipital(sentence, search1, mediaitem='non', TEST='non'):
	#Resets triggers and data failsafes
	v1 = ''
	lmtc = []
	#components from Stanford's Dependency parser to create dep. tree.
	res = depparse.raw_parse(sentence)
	dep = res.__next__()
	ventral_stream = list(dep.triples())
	for tuple in ventral_stream:
		if search1 in tuple[2][0]:
			v1=tuple[0]
		elif search1 in tuple[0][0] and 'cop' in tuple[1]:
			v1=tuple[0]
		elif search1 in tuple[0][0] and 'neg' in tuple[1]:
			v1=tuple[0]
	for tuple in ventral_stream:
		if tuple[0]==v1:
			lmtc.append(tuple)
	corpus_callosum(ventral_stream, v1, lmtc, sentence, mediaitem, TEST) if len(lmtc)>0 else 0



#
##
##Data input and output##
##
#
#The following are .csv reader and output components, including the training
# data builder function (for DNN work later), and the input function for data
# collected in the form of a corpus.
import codecs
import csv

#takes data and saves it to a CSV to build training file.
def Training_Data_Builder(array):
	with codecs.open('/Users/ZaqRosen/Desktop/Thesis_data.csv', 'a', 'utf-8') as csvfile:
		databuilder = csv.writer(csvfile, delimiter=',',
				quotechar='|',
				quoting=csv.QUOTE_MINIMAL)
		databuilder.writerow(array)
	csvfile.close()

#For each corpus in the current study, you need to reset the
# var Listy to include the lexical items of interest.
Listy = ['idea', 'Idea']

#Use the items in this list to classify data according to the media type.
# If the list breaks, remove that item from this list manually.
media_list = ['Written books and periodicals', 'Written miscellaneous', 'Spoken context-governed', 'Spoken demographic', 'Written-to-be-spoken']

#Builds the training data from a printed corpus. Designate your corpus file,
# the search term(s) you’re looking for, and it’ll feed each one to occipital()
# in build mode. 
def pvc(search=Listy, function='build', media_types=media_list):
	read_file = '/Users/ZaqRosen/Desktop/Thesis/Corpora/' + input('Which target referent, sir? ') + '_thesis.txt'
	doc = codecs.open(read_file, 'r', 'utf-8')
	searchlines = doc.readlines()
	doc.close()
	for item in media_types:
		replace_mediaitem = item
		for i, line in enumerate(searchlines):
			if replace_mediaitem in line:
				for item in search:
					if item in line:
						line2 = line.replace('\\', '').replace('}', '').replace('uc0u8232', '').replace('\'92', '\'').replace('a0', '').replace('\'93', '\"').replace('\'94', '\"').replace('\'96', ',').replace('\'97', ',').replace('f0fs24 ', '').replace('cf0 ', '').replace('< ', '').replace(' >', '').replace('\r\n', '').replace('\t', '').replace(replace_mediaitem, '')
						occipital(line2, item, replace_mediaitem, function)



def test(sentence):
	res = depparse.raw_parse(sentence)
	dep = res.__next__()
	ventral_stream = list(dep.triples())
	for tuple in ventral_stream:
		print(tuple)
