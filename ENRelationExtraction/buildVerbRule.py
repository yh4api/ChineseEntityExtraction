# This is just a copy of buildRulesBuy.py/buildRulesBought.py

'''
Syntactic Template Sample Learned Pattern
1. <subj> passive_verb | <subj> was acquired
2. <subj> active_verb | <subj> sold
3. <subj> active_verb dobj | <subj> saw profit
4. <subj> verb infinitive <subj> wanted to sell
5. <subj> auxbe noun <subj> is CEO
6. <subj> auxhave noun <subj> has debt

=======================================

7. active_verb <dobj> sold <dobj>
8. infinitive <dobj> to sell <dobj>
9. verb infinitive <dobj> agreed to buy <dobj>
10. noun auxbe <dobj> CEO is <dobj>
11. noun auxhave <dobj> buyer has <dobj>

=======================================

12. infinitive prep <np> to sell for <np>
13. active_verb prep <np> will sell for <np>
14. passive_verb prep <np> was sold for <np>
15. noun prep <np> owned by <np>

'''
'''
TARGET is/are/was/were/been VBN
TARGET VBP/VBD/VBZ NP
TARGET VBP/VBD/VBZ
TARGET VB* to VB
TARGET is/are/was/were/have/has/had
'''


import re, sys
from pattern.en import lemma, conjugate
exp1 = r"BOUGHT ([^ ]* ){,2}(is|are|was|were|been) (\d*_VBN)" # main is 3rd
# reverse = r'(\d*_NNP) ([^ ]* ){,2}BE TRIGGER'
exp1_h = r"BOUGHT ([^ ]* ){,2}(has|have|had) (\d*_VBN)" # main is 3rd
# reverse = r'(\d*_NNP) ([^ ]* ){,2}HAVE TRIGGER'
exp2 = r"BOUGHT ([^ ]* ){,2}(\d*_VBD|\d*_VBP|\d*_VBZ)" # main is 2nd
#exp2 = "IBM ([^ ]* ){,2}(VBD|VBP|VBZ) "
# reverse = r'(\d*_NNP) ([^ ]* ){,2}TRIGGER'
exp4 = r"BOUGHT ([^ ]* ){,4}\d*_TO (\d*_VB)" # main is 2nd
# reverse = r'(\d*_NNP) ([^ ]* ){,4}\d*_TO TRIGGER'

exp7 = r"(\d*_VBD|\d*_VBP|\d*_VBZ) ([^ ]* ){,1}BOUGHT"
# reverse = r'TRIGGER ([^ ]* ){,1}(\d*_NNP)'
exp8 = r"\d*_TO (\d*_VB) ([^ ]* ){,1}BOUGHT" #main is 1st
# reverse = r'\d*_TO TRIGGER ([^ ]* ){,1}(\d*_NNP)'
exp13 = r"(\d*_VB) (\d*_IN) BOUGHT" #main is same as 14 
exp14 = r"(\d*_VBN) (\d*_IN) BOUGHT"
exp15 = r"(\d*_NN|\d*_NNS) (\d*_IN) BOUGHT"
# reverse = r'TRIGGER ([^ ]* ){,2}(\d*_NNP)'

com1 = re.compile(exp1)
com1_h = re.compile(exp1_h)
com2 = re.compile(exp2)
com4 = re.compile(exp4)
com7 = re.compile(exp7)
com8 = re.compile(exp8)
com13 = re.compile(exp13)
com14 = re.compile(exp14)
com15 = re.compile(exp15)


class ruleBuilder():
	def __init__(self):
		self.fname = ".tmp_pos"
		self.wlist = ["0"]
		self.taglist = []
		self.tverbs = []
		self.seed = []
		self.outFile = ""

	def setOptions(self, optList):
		self.seed = optList["seed"]
		self.outFile = optList["OFile"]
	
	def _reset(self):
		self.wlist = ["0"]
		self.taglist = []
		self.tverbs = []
		self.seed = []
		self.outFile = ""
	def buildRules(self, fname = ".tmp_pos", debug = 0):
		#fname = ".tmp_pos"
		wlist = ["0"]
		taglist = []
		ind = 1
		changed = 0
		tverbs = []
		with open(fname, "r") as fid:
			for line in fid:
				if line == "\n":
					#print " ".join(wlist)
					new_str =  " ".join(taglist)
					#print new_str
					m = com1.search(new_str)
					if m!= None:
						wid = m.group(3).split("_")
						#print wlist[int(wid[0])]
						tverbs.append("BPA"+lemma(wlist[int(wid[0])]))

					m = com1_h.search(new_str)
					if m!= None:
						wid = m.group(3).split("_")
						#print wlist[int(wid[0])]
						tverbs.append("BPE"+lemma(wlist[int(wid[0])]))

					m = com2.search(new_str)
					if m!= None:
						wid = m.group(2).split("_")
						#print wlist[int(wid[0])]
						tverbs.append("BVP"+lemma(wlist[int(wid[0])]))
					m = com4.search(new_str)
					if m!= None:
						wid = m.group(2).split("_")
						#print wlist[int(wid[0])]
						tverbs.append("BVP"+lemma(wlist[int(wid[0])]))

					m = com7.search(new_str)
					if m!= None:
						wid = m.group(1).split("_")
						#print wlist[int(wid[0])]
						tverbs.append("AVP"+lemma(wlist[int(wid[0])]))

					m = com8.search(new_str)
					if m!= None:
						wid = m.group(1).split("_")
						#print wlist[int(wid[0])]
						tverbs.append("AVP"+lemma(wlist[int(wid[0])]))

					m = com13.search(new_str)
					if m!= None:
						wid = m.group(1).split("_")
						inid = m.group(2).split("_")
						#print wlist[int(wid[0])]
						tverbs.append("AVO"+wlist[int(wid[0])]+" "+wlist[int(wid[0])])

					m = com14.search(new_str)
					if m!= None:
						wid = m.group(1).split("_")
						inid = m.group(2).split("_")
						#print m.groups()
						tverbs.append("AVN"+wlist[int(wid[0])]+" "+wlist[int(inid[0])])
					m = com15.search(new_str)
					if m!= None:
						wid = m.group(1).split("_")
						inid = m.group(2).split("_")
						#print m.groups()
						tverbs.append("ANN"+wlist[int(wid[0])]+" "+wlist[int(inid[0])])

					#print "\n"
					wlist = ["0"]
					taglist = []
					ind = 1
				else:
					line = line.rstrip()
					l = line.split("\t")
					if l[0] == "-LRB-":
						l[0] = "("
						changed = 1
					elif l[0] == "-RRB-":
						l[0] = ")"
						changed = 1
					#elif l[0] in ["IBM", "ibm"]:
					elif l[0] in self.seed:
						l[1] = "BOUGHT"
						changed = 1
					elif l[0] in ["is", "are", "was", "were", "been","have", "has", "had"]:
						l[1] = l[0]
						changed = 1
					wlist.append(l[0])
					if changed == 0:
						l[1] = str(ind)+"_"+l[1]
					taglist.append(l[1])
					changed = 0
					ind += 1
		if debug == 1 :
			for s in set(tverbs):
				if tverbs.count(s) > 1:
					print s
		else:
			fout = open(self.outFile, "w")
			for s in set(tverbs):
				if tverbs.count(s) > 1:
					fout.write("%s\n"%s)
			fout.close()
