# input : 100% relevent docs and 100% not relevent docs manually created. In this example, ibm_sl_rel and ibm_sl_irrel respectively, derived from ibm_sl collection.

import REconfig as RC 
from buildVerbRule import ruleBuilder as RB
from subprocess import call

from collections import defaultdict

import sys, re
import csv
from pattern.en import conjugate
	
def PosTagging(fname):
	command = "sh postagger/stanford-postagger.sh "+ fname +" > .tmp_pos"
	call(command, shell = True)

def compareV(fr, fir):
	listrel = set()
	listunrel = set()
	with open(fr, "r") as f1:
		for line in f1:
			line = line.splitlines()[0]
			listrel.add(line)
	with open(fir, "r") as f2:
		for line in f2:
			line = line.splitlines()[0]
			listunrel.add(line)
	return list(listrel - listunrel)

def create_defined_template(arr):
	for x in arr:
		x = x.splitlines()[0]
		if x[2] == "P":
			for t in tenses:
				a = conjugate(x[3:], t)
				triggers[x[0]][x[:3]].append(str(a))
	
		elif x[3:].find(" ") != -1 and x[3:] not in triggers_bi:
			triggers_bi.append(x[3:])
		elif x[:3] in ["BPA", "BPE"] and x[3:] not in triggers_p:
			triggers_p.append(x[3:])
		else:
			triggers["OTHERS"].append(x[3:])


tenses = ["1sg", "3sg", "p"]
reverse={"A":"B", "B":"A"}

def postC(create, line_id, trig, trig_pos, actor, actor_p):
	if create:
		#writeFrame(line_id, trig, trig_pos, actor, actor_p)
		fw = globals()["framewriter"]
		fw.writerow([line_id, trig, trig_pos, actor, actor_p])
	else:
		line_id = str(line_id)
		trig_pos = str(trig_pos)
		#print frames[line_id] if line_id in frames else line_id
		if line_id in frames and trig_pos == frames[line_id][1] and frames[line_id][3]==reverse[actor_p]:
			if actor_p == "B":
				print "FRAME:", actor, trig, frames[line_id][2]
			else:
				print "FRAME:", frames[line_id][2], trig, actor

def printExtPattern(wid, wlist, taglist):
	print " ".join(wlist)
	print " ".join(taglist)
	print wlist[int(wid)-1]
	print ""
ReExpGroup = [r'(\d*_NNP) ([^ ]* ){,2}TRIGGERB', r'(\d*_NNP) ([^ ]* ){,3}\d*_TO TRIGGERB', r'(\d*_NNP) BE TRIGGERP', r'(\d*_NNP) HAVE TRIGGERP', r'TRIGGERA ([^ ]* ){,1}(\d*_NNP)']
ReExtGroup = [1,1,1,1,2]
ReExpType = ["B", "B", "B", "B", "A"]

def read_pos_key_unigram(fname, create, debug = 0):
	wlist = []
	taglist = []
	ind = 1
	changed = 0
	oc = 0
	lineid = 0
	old = ""
	trig = ""
	trig_pos = 0
	with open(fname, "r") as fid:
		for line in fid:
			if lineid > 50000:
				break
			if line == "\n":
				if oc == 1 :
					"""
					m =  re.search(r'(\d*_NNP) ([^ ]* ){,2}TRIGGERB', " ".join(taglist))
					if m != None:
						wid = m.group(1).split("_")[0]
						if debug:
							printExtPattern
						postC(create, lineid, trig, trig_pos, wlist[int(wid)-1], "B")
					"""			
					for exp, expIn, expType in zip(ReExpGroup, ReExtGroup, ReExpType):
						m = re.search(exp, " ".join(taglist))
						if m!=None:
							wid = m.group(expIn).split("_")[0]
							if debug:
								printExtPattern(wid, wlist, taglist)
							postC(create, lineid, trig, trig_pos, wlist[int(wid)-1], expType)

					

				wlist = []
				taglist = []
				ind = 1
				changed = 0
				oc = 0
				lineid +=1
				old = ""
				trig = ""
				trig_pos = 0
			else:
				line = line.rstrip()
				l = line.split("\t")
				
				if l[0] in triggers["A"]["AVP"] and l[1] in ["VBP", "VBZ", "VBD"]:
					l[1] = "TRIGGERA"
					changed = 1
					oc = 1
					trig = l[0]
					trig_pos = ind
					

				if l[0] in triggers["B"]["BVP"] and l[1] in ["VBP", "VBZ", "VBD"]:
					l[1] = "TRIGGERB"
					changed = 1
					oc = 1
					trig = l[0]
					trig_pos = ind

				elif l[0] in triggers["OTHERS"]:
					l[1] = "TRIGGER"
					changed = 1
					oc = 1
					trig = l[0]
					trig_pos = ind

				elif l[0] in triggers_p and l[1] in ["VBN"]:
					l[1] = "TRIGGERP"
					changed = 1
					oc = 1
					trig = l[0]
					trig_pos = ind

				elif l[0] in ["is", "are", "was", "were"]:
					l[1] = "BE"
					changed = 1
					oc = 2
	
				elif l[0] in ["has", "have", "had"]:
					l[1] = "HAVE"
					changed = 1
					oc = 2

				if changed == 0:
					l[1] = str(ind)+"_"+l[1]

				#old = l[0]
				wlist.append(l[0])
				taglist.append(l[1])
				changed = 0
				ind += 1

def read_pos_key_bigram(fname, create, debug = 0):
	wlist = []
	taglist = []
	ind = 1
	changed = 0
	oc = 0
	lineid = 0
	old = ""
	trig = ""
	trig_pos = 0
	with open(fname, "r") as fid:
		for line in fid:
			if lineid > 50000:
				break
			if line == "\n":
				if oc == 1:
					m =  re.search(r'TRIGGER ([^ ]* ){,2}(\d*_NNP)', " ".join(taglist))
					if m != None:
						wid = m.group(2).split("_")[0]
						if debug:
							printExtPattern(wid, wlist, taglist)
						postC(create, lineid, trig, trig_pos, wlist[int(wid)-1], "A")

				wlist = []
				taglist = []
				ind = 1
				changed = 0
				oc = 0
				lineid +=1
				old = ""
				trig = ""
				trig_pos = 0
			else:
				line = line.rstrip()
				l = line.split("\t")
				cand = old+" "+l[0]
				if cand in triggers_bi:
					l[1] = "TRIGGER"
				
					taglist.pop()
					changed = 1
					oc = 1
					trig = l[0]
					trig_pos = ind
				elif l[0] in ["is", "are", "was", "were"]:
					l[1] = "BE"
					changed = 1
					oc = 2

				elif l[0] in ["has", "have", "had"]:
					l[1] = "HAVE"
					changed = 1
					oc = 2

				if changed == 0:
					l[1] = str(ind)+"_"+l[1]

				old = l[0]
				wlist.append(l[0])
				taglist.append(l[1])
				changed = 0
				ind += 1



if __name__ == "__main__":
	RB1 = RB()
	arg = {}
	doer = [x[0] for x in RC.seed["ibm"]]
	doee = [x[1] for x in RC.seed["ibm"]]
	
	"""
	#Step1
	PosTagging(RC.relInput)

	arg = {"seed":doer, "OFile":RC.relActiveOut}
	RB1.setOptions(arg)
	RB1.buildRules()
	RB1._reset()
	arg = {"seed":doee, "OFile":RC.relPassiveOut}
	RB1.setOptions(arg)
	RB1.buildRules()
	RB1._reset()

	PosTagging(RC.irrelInput)
	arg = {"seed":doer, "OFile":RC.irrelActiveOut}
	RB1.setOptions(arg)
	RB1.buildRules()
	RB1._reset()

	arg = {"seed":doee, "OFile":RC.irrelPassiveOut}
	RB1.setOptions(arg)
	RB1.buildRules()
	RB1._reset()
	"""
	#look for candidate
	compareGroup = [[RC.relActiveOut, RC.irrelActiveOut], [RC.relPassiveOut, RC.irrelPassiveOut]]

	for doBoth in [0, 1]:
		triggers = {}
		triggers["A"] = defaultdict(list)
		triggers["B"] = defaultdict(list)
		triggers["OTHERS"] = []
		triggers_bi = []
		triggers_p = []


		frames = {}
		vlist = compareV(compareGroup[doBoth][0], compareGroup[doBoth][1])
		create_defined_template(vlist)
		if doBoth:
			#read frame
			fid = open("frame.csv", "rb")
			framereader = csv.reader(fid, delimiter="\t", quotechar = "|")
			for row in framereader:
				frames[row[0]] = row[1:]
		else:
			fid = open("frame.csv", "wb")
			framewriter = csv.writer(fid, delimiter="\t", quotechar = "|", quoting=csv.QUOTE_MINIMAL)

		#To combine two relations
		#If False, write only. if True, compare

		read_pos_key_unigram("iot-train.pos", not doBoth)#iot-train.pos is test corpus, created in advance.
		read_pos_key_bigram("iot-train.pos", not doBoth)	
	
		fid.close()

