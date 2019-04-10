from __future__ import division 
import os
import sys
import numpy as np
import glob
import collections
from collections import Counter, defaultdict
import re
import json
import math


def tokenize(sett):
    s=[ x for x in sett if x.isalpha()]
    return s

if __name__=='__main__':
    nbmodel= open("nbmodel.txt","r")
	temp= nbmodel.readline()
	#classes
	classes=[]
	for _ in range(4):
		classes.append(nbmodel.readline()[:-1])
	
	tempv=nbmodel.readline()
	vocabline=nbmodel.readline()
	#vocab
	vocablist= vocabline.split(" ")
	vocablist= vocablist[:-1]
	#priors
	priorline= nbmodel.readline()
	jpriors= eval(priorline)
	priorsdict=defaultdict(float)
	#           print(jpriors['priors'])
	#priorsdict
	for c in classes:
		priorsdict[c]=jpriors["priors"][c]
	print(priorsdict)
	#cp
	cpline= nbmodel.readline()
	jcp= eval(cpline)
	all_files_test = glob.glob(os.path.join(directory, '*/*/fold1/*.txt'))
	
	test_by_class = collections.defaultdict(list)

	#getting vocab
	w=[]
	opfile=open("nboutput.txt","w")
	for f in all_files_test:
		flets=set(re.findall(r'\w+', open(f).read().lower()))
		ftokens=tokenize(flets)
		neww=[x for x in ftokens if x in vocablist]
		scores=[0.0 for _ in range(4)]
		for i in range(len(classes)):
			scores[i]= math.log(priorsdict[classes[i]])
			for terms in neww:
				scores[i] += math.log(jcp[terms][i][1])
		myclass=classes[scores.index(max(scores))]
		classwords= myclass.split('_')
		opfile.write(str(classwords[1])+' '+ str(classwords[0])+' '+ f + '\n')
	opfile.close()
		
		


	

    


