from __future__ import division
import os
import sys
import numpy as np
import glob
import collections
from collections import Counter, defaultdict
import re
import json

def tokenize(sett):
    s=[ x for x in sett if x.isalpha()]
    return s
	
if __name__=='__main__':

	all_files = glob.glob(os.path.join(sys.argv[1], '*/*/*/*.txt'))
	train_by_class = collections.defaultdict(list)

	#getting vocab
	vocab=set([])
	for f in all_files:
		flets=set(re.findall(r'\w+', open(f).read().lower()))
		ftokens=tokenize(flets)
		for tokens in ftokens:
			vocab.add(tokens)
		
		class1, class2, fold, fname = f.split(os.path.sep)[-4:]
		class1= class1.split('_')[0]
		class2= class2.split('_')[0]
		#remeber to alter this later while running on vocarium
		if  fold =='fold1':
			continue
			
		else:
			train_by_class[class1+'_'+class2].append(f)
	trainjson=json.dumps(train_by_class, indent=2)

	vlen= len(vocab)
	vocablist= list(vocab)
	jltrain= json.loads(trainjson)
	listjtrain= list(jltrain.items())  


	#getting N
	num_train=0
	for clss in listjtrain:
		num_train += len(clss[1])

	#getting classes
	classes= [ x[0] for x in listjtrain]

	#intializing priors and condtptob

	priors=defaultdict(float)
	condprob= defaultdict(list)
	
	for c in classes:
		nc=len(jltrain[c])
		tp= float(nc)/float(num_train)
		priors[c]= tp
		cls_dirs= jltrain[c]
		classwords=[]
		for path in cls_dirs:
			classwords = classwords + tokenize(re.findall(r'\w+', open(path).read().lower()))
		numtc= len(classwords)
		
		for v in vocab:
			condname= "p(" + str(v) + "/" + str(c) + ")"
			freq=classwords.count(v)
			cp= (freq + 1)/(vlen + numtc)
			templist= [condname, cp]
			condprob[v].append(templist)
			
	priorp= {"priors": priors}
	condprobp= {"condprob": condprob}
	
	with open('nbmodel.txt','w') as output:
		output.write("classes: "+"\n")
		for cl in classes:
			output.write(str(cl) + "\n")
		output.write("vocab: "+"\n")
		for v in vocablist:
			output.write(v + " ")
		output.write("\n")
		output.write(json.dumps(priorp))
		output.write('\n')
		output.write(json.dumps(condprob))

	output.close()

