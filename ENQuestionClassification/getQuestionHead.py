# Implementation of From symbolic to sub-symbolic information in question classification
# 2016.06.14
import sys
import re
#from nltk import Tree
from nltk import ParentedTree
import xml.etree.ElementTree as ET

"""
example:
given a question => "what are the landmarks of capital in Taiwan"
expected head => "landmarks"

"""
syntac_sen = "(ROOT (SBARQ (WHNP (WDT What) (NN county)) (SQ (VBZ is) (NP (NNP Modesto) (, ,) (NNP California)) (PP (IN in))) (. ?)))" 
syntac_sen_ans = '{"ROOT":[{"SBARQ":[{"WHNP":[{"WDT":"What"}, {"NN":"county"}]}, {"SQ" :[{"VBZ":"is"},{"NP":[{"NNP":"Modesto"},{",":","},{"NNP":"California"}]} ,{"PP":[{"IN":"in"}]}]} ,{".":"?"}]}]}'
head_trace_rule ={
  "S":[["L", "VP", "FRAG", "SBAR", "ADJP", "UCP", "TO"], ["R", "NP"]],
  "SQ":[["L", "NP", "VP", "SQ"]],
  "NP":[["RBP", "NP", "NN", "NNP", "NNPS", "NNS", "NX", "JJR"], ["R", "NP", "PRP"], ["RBP", "$", "ADJP", "PRN"], ["R", "CD"], ["RBP", "JJ", "JJS", "RB", "QP", "DT", "WDT", "RBR", "ADVP"], ["L", "POS"]],
  "PP":[["L", "WHNP", "NP", "WHADVP", "SBAR", "S"], ["R", "IN", "TO", "VBG", "VBN", "RP", "FW"], ["L", "PP"]],
  "WHNP":[["L","NP"], ["RBP", "NN", "NNP", "NNPS", "NNS", "NX", "POS", "JJR"], ["RBP", "$", "ADJP", "PRN"], ["R", "CD"], ["RBP", "$", "JJ", "JJS", "RB", "QP"],["L", "WHNP", "WHADJP", "WP$", "WP", "WDT"]],
  "WHPP":[["R","WHNP", "WHADVP", "NP", "SBAR"]],
  "VP":[["R", "WHPP", "PP", "WHNP"],["L", "S", "ADJP", "NN", "NNS", "NNP", "NP", "VP"]],
  "SINV":[["L", "NP", "VP", "S", "SINV", "ADJP", "VBZ", "VBD", "VBP", "VB", "MD"]],
  "SBARQ":[["L", "SQ", "S", "SINV", "SBARQ", "FRAG"]],
  "WHADVP":[["R", "RB", "JJ"]], 
  "WHADJP":[["L", "ADJP", "JJ", "WRB", "CC"]],
  "FRAG":[["L", "SBAR", "S", "SQ", "SINV", "ADJP", "ADVP", "FRAG"]]
  }

#print head_trace_rule["SBARQ"]
"""
#tried to parse parenthesed tree without wordnet package

exp = '(.*?)\((.*)\)(.*)'
prog = re.compile(exp)

def get_kids(text):
	if text.startswith("("):
		pass
	elif text.endswith(")"):
		pass
	else:
		pass


def print_json(text, level):
	if text.startswith("("):
		#out.write("\"data\":{\"type\":\""+text[2:]+"\"}, \"children\":[{")
		out.write("\""+text[1:]+"\":{")
	elif text.endswith(")"):
		print_json(text[:-1], level+1)
		#out.write("}]")
		out.write("}")
		if level == 0:
			#out.write("},{")
			out.write(",")
	else:
		#out.write("\"data\":{")
		#out.write("\"word\":\""+text+"\", \"type\":\"TK\"")
		out.write("\""+text+"\":1")
		#out.write("}, \"children\":[]")

def get_head(text):
	text = text.rstrip()
	text = re.sub(r'\s', ' ', text)
	text = re.sub(r' {2,}', ' ', text)
	ts = text.split()
	for t in ts	:
		print_json(t, 0)
	#return get_head()

def replace_head(text):
	text = text.rstrip()	
	text = re.sub(r'\s', ' ', text)
	text = re.sub(r' {2,}', ' ', text)
	print text
	#text = text.replace(')) (', ")},{\"")
	text = text.replace(')) (', "),{\"")
	#text = text.replace(") (", "\"},{\"")
	text = text.replace(") (", "\",\"")
	print text
	text = text.replace(" (", "\":{\"")
	print text
	text = re.sub(r"([^)])\)", r'\1"}', text)
	print text
	text = text.replace(")", "}")
	print text
	text = text.replace("(", "{\"")
	print text
	text = text.replace(" ", "\":\"")
	print text
	return text
"""
def LookByL(subtree, rule):
	#print "LookByL", subtree
	l = len(subtree)
	for r in rule:
		for sb in subtree:
			if sb.node == r:
				return sb	
	#return subtree[0]
	return ""

def LookByR(subtree, rule):
	l = len(subtree)
	#print "LookByR", subtree
	for r in rule:
		for j in range(l-1, -1, -1) :
			sb = subtree[j]
			if sb.node == r:
				return sb	
	#return subtree[-1]
	return ""

def LookByRBP(subtree, rule):
	l = len(subtree)
	#print "LookByRBP", subtree
	for j in range(l-1, -1, -1):
		sb = subtree[j]
		if sb.node in rule:
			return sb	
	#return subtree[-1]
	return ""

def LookByLBP(subtree, rule):
	l = len(subtree)
	for sb in subtree:
		if sb.node in rule:
			return sb	

	#return subtree[0]
	return ""


def getHead(syntac_sen):
	t = ParentedTree(syntac_sen.text)


	target = t[0]

	while target.height() != 2:
		### non-trivial rules: no.1 
		flag = 0
		parent = target
		if target.node == "SBARQ":
			for ts in target:
				if ts.node in ["WHNP", "WHPP", "WHADJP", "WHADVP"] and len(ts) > 1:
					
					target = ts
					flag = 1
					break	
		###
		if not flag:
			rules = head_trace_rule[target.node]
			#rules = head_trace_rule.get(target.node, [])
			for rule in rules:
				if rule[0] == "L":
					newTarget = LookByL(target, rule[1:])
				elif rule[0] == "R":
					newTarget = LookByR(target, rule[1:])
				elif rule[0] == "LBP":
					newTarget = LookByLBP(target, rule[1:])
				elif rule[0] == "RBP":
					newTarget = LookByRBP(target, rule[1:])
				if newTarget != "":
					break
			if newTarget == "":
				target = target[0]
			else:
				target = newTarget
			#print target
			#print target.height()
		
		### non-trivial rules: no.2:
		if flag:
			leafPos = getLeafPOS(target)
			m = re.search(r'(NN|NNS)_(\d+) POS_', leafPos)
			if m != None:
				lvs = target.leaves()
				print m.groups()
				target = ParentedTree("("+m.group(1)+" "+lvs[int(m.group(2))]+")")

		### non-trivial rules: no.3
		
		if target.height() == 2 and target.leaves()[0] in ["name", "kind", "type", "genre", "group", "part"]:
			print parent
			for k in parent:
				if k.node == "PP":
					target = k
					break
			pr = parent.right_sibling()
			for p in pr:
				if pr.node == "PP":
					target = pr
					break
				
	return target.leaves()[0]

def getLeafPOS(t):
	
	wid = 0
	ws = []
	for s in t.subtrees(lambda t: t.height()==2):
		ws.append(s.node+"_"+str(wid))
		wid += 1
	return " ".join(ws)

	



if __name__ == "__main__":
	"""
	input has to be a CORENLP parsed file
	"""
	tree = ET.parse("/home/yhlin/corenlp/outputXML/input.xml")
	sens = tree.getroot().find("./document/sentences")



	fid = open("/home/yhlin/corenlp/raw_text/input", "r") 
	for s in sens:
		orig_s = fid.readline()
		ss = s.find("./parse")
		#t = Tree(ss.text)
		#print t.leaves() 
		h = getHead(ss)
		#word_sense = simple_lesk(orig_s, h, "n")
		print orig_s, h

	fid.close()

#content_word = ["Netherlands"]


