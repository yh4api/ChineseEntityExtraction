# -*- coding:utf-8 -*-

import re, os, sys
import xml.etree.ElementTree as ET
special = "#*?!@%&$+(){}[]"
special_exp = r'[#!@%&\+\$\*\?\(\)\{\}\[\]]'
tree = ET.parse("concept.xml")
root = tree.getroot()
fout = open("a.out", "w")
for concepts in root.findall("c"):
	defi = []
	word = concepts.get("w").encode("utf-8")
	definition = concepts.get("d").encode("utf-8")
	defs = definition.split(",")
	for d in defs:
		dplus = re.sub(special_exp, "", d)
		if "=" in dplus:
			dplus = dplus.partition("=")[2]
		tmp = dplus.split("|")
		for t in tmp:
			defi.append(t+"#NN#"+t)

	fout.write(word+"; ")
	fout.write("  ".join(defi))
	fout.write("\n\n")

fout.close()
