#20160121, the idea comes from Wordnet Sring Inclusion in Taxonomy Construction Using Syntactic Contextual Evidence

import csv
from nltk.corpus import wordnet as wn

import re

import sys
from subprocess import call
file_id = 0

from networkx import networkx as nx
from networkx.readwrite import json_graph 

#Step1 : Term Extraction and Taxonomic Relation Identification 
 
#data is given, ignore data with scores not equal than 0

def readCSV(filename):
	new_arr = []
	with open(filename, "r") as f:
		reader = csv.reader(f, delimiter = ",")
		for row in reader:
			if row[1] == "0.0000000000":
				break
			new_arr.append(row[0])
	
	return new_arr


comp_verb = re.compile(r"ly_[^_]*ed$") #filter terms like "highly_praised", most of them are verbs.

#Param = toOutput
#0: no output, just return terms have relations to others
#1: output to screen, and return terms have relations to others
#2: output to file, and return terms have relations to others
def WNSimilarity(termArr, toOutput = 1):
	#print len(termArr)
	fout = None
	if toOutput == 2:
		fout = open("file"+str(file_id)+"_out1", "w")
	termsHere = set()
	t1_id = 0 
	for t1 in termArr[0:-1]:
		t2_id = t1_id+1
		for t2 in termArr[t2_id:]:
			try:
				score = wn.synsets(t1, wn.NOUN)[0].path_similarity(wn.synsets(t2, wn.NOUN)[0])
				if score >= 0.24:
					if toOutput == 1:
						print t1, t2, score 
					elif toOutput == 2 and fout != None:
						fout.write("%s %s %f\n"%(t1, t2, score))
					termsHere.add(t1)
					termsHere.add(t2)
			except:
				pass
		t1_id += 1
	if fout != None:
		fout.close()
	return list(termsHere)
"""
@stemRecover: use term in the list with shortest length instead of unreadable stem
ex: ha => [has, have, having, had]
output: has => [has, have, having, had]
"""
def stemRecover(key, valueArray):
	if key in valueArray:
		return key
	else: #choose term in the list with shortest length
		min_len = 500 
		tmpk = ""
		for v in valueArray:
			if len(v) < min_len:
				min_len = len(v)
				tmpk = v

		return tmpk

def itemSelect(valueArray):
	newA = []
	for v in valueArray:
		if comp_verb.search(v) == None and "_" in v:
			newA.append(v)

	return newA

def extractHeadWords(termArr, toOutput = 2):
	from nltk.stem.snowball import SnowballStemmer
	newArr = {}
	newArrS = {}
	stemGroup = {}
	scoreArr = {}
	notInWN = []	
	neverNounGroup = []
	allTerms = []
	
	stemmer = SnowballStemmer("english")
	print "Step1: create head word similarity list: threshold 0.25"
	for t1 in termArr:
		tmp = t1.rsplit("_", 1)
		
		
		neverN = 1
		if tmp[-1] in neverNounGroup:
			continue
		elif tmp[-1] not in allTerms:
			if wn.synsets(tmp[-1]) == []:
				neverN = 0
				notInWN.append(t1)
			for sy in wn.synsets(tmp[-1]):
				if ".n." in sy.name:
					neverN = 0
					break
			allTerms.append(tmp[-1])
			if neverN == 1 :
				neverNounGroup.append(tmp[-1])
				continue

		
	inWN = set(allTerms) - set(neverNounGroup) - set(notInWN)
	hasToBeHead = WNSimilarity(sorted(list(inWN)), toOutput)
	#return 0
	#example: dictact, dictation, command
	#Wordnet group dictation and command together while string inclusion put dictact and dictation together
	#hasToBeHead stores dictation and command to make sure dictation can be an independent entry.
	print "Step2: create group by string inclusion"
	
	for t1 in termArr:
		tmp = t1.rsplit("_", 1)
		if tmp[-1] in neverNounGroup:
			continue

		if tmp[-1] in hasToBeHead:
			newArr[tmp[-1]] = 1
			newArrS.setdefault(tmp[-1], [])
			newArrS[tmp[-1]].append(t1)
		else:
			stem = stemmer.stem(tmp[-1])
			newArr[stem] = 1
			newArrS.setdefault(stem, [])
			newArrS[stem].append(t1)
	if toOutput == 1: #output to screen
		print len(newArr)
		for k in sorted(newArr.keys()):
			print stemRecover(k, newArrS[k]), itemSelect(newArrS[k]) #out2
	elif toOutput == 2:
		with open("file"+str(file_id)+"_out2", "w") as fout:
			for k in sorted(newArr.keys()):
				fout.write(stemRecover(k, newArrS[k]))
				fout.write(" ")
				fout.write(itemSelect(newArrS[k]).__str__())
				fout.write("\n")
		 
#example: dialog = dialogue
#combine entries with dialog/dialogue together and eliminate dups
def modifyIndex(fname, toOutput = 2):
	print "step3: modify index"
	equivSet = []
	new_indset = {}
	with open(fname, "r") as f1:
		for line in f1:
			tmp = line.rstrip().split(" ")
			if int(float(tmp[2])) == 1:
				check = 0
				for e in equivSet:
					if tmp[0] in e or tmp[1] in e:
						check = 1
						e += tmp[:2]
						break
				if check == 0:
					equivSet.append(tmp[:2])
					
	"""
	example: dialog dialogue 1
	dialog conversation 0.5
	dialogue conversation 0.5
	==>
	dialog_dialogue dialog_dialogue 1
	dialog_dialogue conversation 0.5
	dialog_dialogue conversation 0.5 <= eliminate this by awk
	"""
	for e in equivSet:
		e = list(set(e))
		#print set(e)
		for ind in e:
			new_indset[ind] = "_".join(e)
	
	with open(fname, "r") as f1:
		if toOutput == 1:
			for line in f1:
				tmp = line.rstrip().split(" ")
				ab = map(lambda x: new_indset.get(x, x), tmp)
				print " ".join(ab)
		elif toOutput == 2:
			tmpfile = "tmpfile"+str(file_id)+"_out3"
			truefile = "file"+str(file_id)+"_out3"
			fout = open(tmpfile, "w")
			for line in f1:
				tmp = line.rstrip().split(" ")
				if float(tmp[-1])==1:
					continue
				ab = map(lambda x: new_indset.get(x, x), tmp)
				fout.write((" ".join(ab)).__str__())
				fout.write("\n")
			fout.close()
			command = "awk '!x[$0]++' < "+tmpfile+" >"+truefile
			res = call(command, shell=True)	

def addGraph(fname, toOutput = 2):
	
	G = nx.Graph()
	with open(fname, "r") as f1:
		for line in f1:
			tmp = line.strip().split(" ")
			G.add_edge(tmp[0], tmp[1])
	fout = open("file"+str(file_id)+"_out4", "w")
	for g in nx.connected_components(G):
		if toOutput!=2:
			print g 
		else:
			fout.write(g.__str__()+"\n")
	fout.close()		
	return G

synonym = {}

def checkSynonym(w):
	global synonym
	if "_" not in w:
		return w
	else:
		ws = w.split("_")
		for wss in ws[:-1]:
			synonym[wss] = ws[-1]
		return ws[-1]

def outputSynonym(s, filename = "synonym.txt"):
	with open(filename, "w") as f1:
		for syn in s:
			f1.write("%s %s\n"%(syn, s[syn]))

def readSynonym(filename):
	synonym = {}
	if filename == "":
		pass
	else:
		with open(filename, "r") as f1:
			for line in f1:
				tmp = line.rstrip().split()
				synonym[tmp[0]] = tmp[1]
	
	return synonym


"""
@hiddenHypo compares each hypernym paths of each word synset.
run hiddenHypo(["league", "school","institute", "univesity", "college", "academy"]) to see the result
threshold is :
> 3 for hypernym max_depth; less than 3 is too abstract
< 4 between target synset and hypernym; greater than four means too far; pairs are taken into consideration only when distance(h, a) and distance(h, b) are both less than this threshold. 
< 3 is set for sum(total_distance)/len(v), this threshold is propotional to last threshold. this value will always less than last one.
this function applies on the top level nodes now, the deeper it applies, the bigger the first threshold and the smaller the rest of them should be set.
"""
def hiddenHypo(itemArr, debug=False):
	iid = 0
	hy_mx = [[[0,0] for a in range(len(itemArr))] for b in range(len(itemArr))]
	hypers = []
	potential_hidden = {}
	depth_hidden = {}
	total_distance = {}
	#for wi in itemArr:
	#	tmp_hy = [s.hypernym_paths() for s in wn.synsets(s)]
	#	hypers.append(flatten(tmp_hy))
	for i in range(0, len(itemArr)-1):
		for j in range(i+1, len(itemArr)):
			maxT = [0 , 0, 50, 50]
			#tmp3 = 50
			#tmp4 = 50
			for x in wn.synsets(itemArr[i]):
				for y in wn.synsets(itemArr[j]):
					#print itemArr[i],itemArr[j], x.lowest_common_hypernyms(y)
					try:
						chy = x.common_hypernyms(y)
						
						tmpchy = max([s.max_depth() for s in chy])
						if tmpchy > maxT[0]:
							maxT[0] = tmpchy
							cy = [s for s in chy if s.max_depth() == maxT[0]]
							maxT[1] = cy[0].name.split(".")[0]
							xin = min([len(xp)-xp.index(cy[0]) for xp in x.hypernym_paths() if cy[0] in xp])
							#print xin
							yin = min([len(yp)-yp.index(cy[0]) for yp in y.hypernym_paths() if cy[0] in yp])
							#print type(yin), maxT[3], j
							maxT[2] = min([maxT[2], xin])
							maxT[3] = min(maxT[3],  yin)
						#print "End of try"				
					except:
						#print sys.exc_info()
						pass
			#print i,j, itemArr[i], itemArr[j], maxT
			if maxT[0] >= 3 and maxT[2] <= 4 and maxT[3] <= 4:
				potential_hidden.setdefault(maxT[1], set())
				potential_hidden[maxT[1]].add(itemArr[i])
				potential_hidden[maxT[1]].add(itemArr[j])
				total_distance.setdefault(maxT[1], [0 for m in range(len(itemArr))])
				total_distance[maxT[1]][i]= maxT[2]
				total_distance[maxT[1]][j]= maxT[3]
				depth_hidden[maxT[1]] = maxT[0]	
						
	#print itemArr,"\n", hy_mx
	if debug:
		print itemArr
		for k, v in sorted(depth_hidden.items(), key=lambda k:k[1]):
			#print k, v, potential_hidden[k]
			print k in itemArr, k, v, potential_hidden[k], sum(total_distance[k]),"/",len(potential_hidden[k])
	for k, v in potential_hidden.iteritems():
		if float(sum(total_distance[k]))/len(v) > 3:
			potential_hidden[k]=set()
	return potential_hidden

def checkHypernymWNBeta(itemArr, rootid, fp = None, debug = False):
	global synonym
	itemArr = map(checkSynonym, itemArr)
	tmpItemArr = itemArr
	allHypoHyper = set()
	hypo = {}
	iid = 0
	for i in itemArr[0:-1]:
		iid += 1
		for j in itemArr[iid:]:
			#print i, j
			h = isRelated(i, j)
			if h != None and (h in itemArr):
				allHypoHyper.add(h)
				hypo.setdefault(h, [])
				if h != i:
					hypo[h].append(i)
				if h != j:
					hypo[h].append(j)
	DG = nx.DiGraph()
	in_edge = set()

	#kk = hypo.keys()
	for k, v in hypo.iteritems():
		#print k, set(v)
		for vs in list(set(v)):
			if vs not in in_edge:
				DG.add_edge(k, vs)
				in_edge.add(vs)
			if vs in tmpItemArr:
				tmpItemArr.remove(vs)

	#hiddenNodes = hiddenHypo(hypo.keys())
	hiddenNodes = hiddenHypo(tmpItemArr)
	dup = set()
	hid = 1
	for k, v in sorted(hiddenNodes.iteritems(), key=lambda k:len(k[1]), reverse=True):
		if debug:
			print "K", k, v, tmpItemArr
		#continue
		if v == set(tmpItemArr):
			break

		vt = v - dup
		#dup.update(v)
		if len(vt) <= 1:
			#dup.update(vt)
			continue
		if k in itemArr:
			#print "k = ", k, vt
			#dup.discard(k)
			vt.discard(k)
			for vs in vt:
				DG.add_edge(k, vs)
		else:
			for vs in vt:
				DG.add_edge(str(rootid)+"_Hidden"+str(hid), vs)
				
			hid += 1
		dup.update(vt)
	
	for t in tmpItemArr:		
		if t not in dup:
			DG.add_edge("Root"+str(rootid), t)
	
	for l in range(1, hid):
		DG.add_edge("Root"+str(rootid), str(rootid)+"_Hidden"+str(l))
	if fp != None:
		try:
			
			fp.write(json_graph.tree_data(DG, "Root"+str(rootid)).__str__()+"\n")
			
		except:
			fp.write(nx.to_dict_of_lists(DG).__str__()+"\n")
			nx.write_gml(DG,"out.gml")

	else:
		try:
			print json_graph.tree_data(DG, "Root"+str(rootid))
		except:
			print nx.to_dict_of_lists(DG)
			nx.write_gml(DG,"out.gml")
	
def isRelated(a , b):
	syn_a = wn.synsets(a)[0]
	syn_b = wn.synsets(b)[0]
	try:
		common_hyper = syn_a.lowest_common_hypernyms(syn_b)
		hy = common_hyper[0].name.split(".",1)
		return hy[0]
	except:
		return None

def groupHyperTry(NG):
	fout = open("file"+str(file_id)+"_out5", "w")
	root_id = 1
	for g in nx.connected_components(NG):
		checkHypernymWNBeta(g, root_id, fout)
		root_id += 1
	fout.close()

def groupHyperBeta(fname):
	fout = open("file"+str(file_id)+"_out5", "w")
	with open(fname, "r") as f1:
		root_id = 1
		for line in f1:
			x = eval(line)
			checkHypernymWNBeta(list(x), root_id, fout)
			root_id += 1
	fout.close()

def level1Nodes():
	filename = "file"+str(file_id)+"_out2"
	tmpgraph = {}
	global synonym
	if synonym == {}:
		synonym = readSynonym("synonym.txt")

	with open(filename, "r") as f1:
		for line in f1:
			tmp = line.strip().split(" ", 1)
			key = tmp[0].rsplit("_", 1)[-1]
			tmpgraph[key] = eval(tmp[1])

	"""
	ex: lab = laboratory
	lab = ["bell_lab", "apple_lab"]
	laboratory = ["MIT laboratory"]
	output:
	lab += laboratory, del laboratory
	"""	
	for syn, val in synonym.iteritems():
		tmpgraph[val] += tmpgraph[syn]
		del tmpgraph[syn]


	return tmpgraph

def level2Nodes(filename):
	
	DG = nx.DiGraph()
	with open(filename, "r") as f2:
		for line in f2:
			di = eval(line)
			TG = json_graph.tree_graph(di)
			DG.add_edges_from(TG.edges())

	return DG

def combineEverything(fname, allNodes, toOutput = 2):
	DG = level2Nodes(fname)
	DGN_s1Nodes = DG.nodes()
	tmpDict = level1Nodes()
	for n in DGN_s1Nodes: #ex: Root1: {science:{[psychology, linguistics]}}
		if n in tmpDict:
			#print n, type(tmpDict[n]) == list
		
			for v in tmpDict[n]:
				DG.add_edge(n, v)
			del	tmpDict[n]

	###print nodes have hierachy but not grouped
	"""
	for k, vd in tmpDict.iteritems():
		if len(vd) > 1:
			for v in vd:
				DG.add_edge(k , v)
			DG.add_edge("ROOT0", k)
	"""
	###

	DGN_s2Nodes = DG.nodes()
	isolatedNodes = allNodes - set(DGN_s2Nodes)
	for d in DGN_s2Nodes:
		if d.startswith("Root"):
			#print d, DG.neighbors(d)
			DG.add_edge("ROOT0", d)
			#print DG.neighbors("ROOT0")

	DG2 = nx.DiGraph()
	for sn in isolatedNodes:
		DG2.add_edge("ROOT0", sn)
		#if sn in DG.nodes():
		#	DG.remove_node(sn)
	if toOutput == 2:
		try:
			tmpout1 = str(json_graph.tree_data(DG, "ROOT0")).replace("'id'", "'name'")
			out1 = "var data1 ="+tmpout1+";"
			tmpout2 = str(json_graph.tree_data(DG2, "ROOT0")).replace("'id'", "'name'")
			out2 = "var data2 ="+tmpout2+";"
			fout = open("file"+str(file_id)+"_final.js", "w")
			fout.write(out1+"\n"+out2)
			fout.close()
		except:
			nx.write(DG, "out.gml")	
	else: 
		try:
			print json_graph.tree_data(DG, "ROOT0")
			print json_graph.tree_data(DG2, "ROOT0")
		except:
			nx.write_gml(DG,"out.gml")


if __name__ == "__main__":
	 
	salient_terms = readCSV("salient.csv")
	extractHeadWords(salient_terms, 2) # > _out1, _out2
	modifyIndex("file"+str(file_id)+"_out1", 2) # < _out1 > _out3
	NG = addGraph("file"+str(file_id)+"_out3") # < _out3 > _out4
	#groupHyperTry(NG)
	groupHyperBeta("file"+str(file_id)+"_out4") # < _out4 > _out5
	#outputSynonym(synonym)
	combineEverything("file"+str(file_id)+"_out5", set(salient_terms)) # < _out5 > _final
