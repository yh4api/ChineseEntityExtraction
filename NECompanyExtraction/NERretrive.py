import re

exp1 = r'((\d*_NNP |\d*_NNPS ){2,})'
exp2 = r'(_\w+ (\d*_NNP|\d*_NNPS)) \d*_[^N]'
comp1 = re.compile(exp1)
comp2 = re.compile(exp2)
fname = "NER-train.pos"
def way2(fname):
	with open(fname, "r") as fid:
		ind = 1
		wlist = []
		taglist = []
		lineid = 0
		for line in fid:
			if lineid > 4000:
				break
			if line == "\n":
				lineid += 1
				new_str = " ".join(taglist)
				m = re.split(r'(\d*_NNPS? )+', new_str)
				print new_str
				print m
				ind = 1
				wlist = []
				taglist = []
				
			else:
				line = line.rstrip()
				l = line.split("\t")
				l[1] = str(ind)+"_"+l[1]
				wlist.append(l[0])
				taglist.append(l[1])
				ind += 1
#way2(fname)
def way1(fname):
	with open(fname, "r") as fid:
		ind = 1
		wlist = []
		taglist = []
		lineid = 0
		for line in fid:
			if lineid > 4000:
				break
			if line == "\n":
				lineid +=1
				print " ".join(wlist)
				print ""
				new_str = " ".join(taglist)
				#m1 = comp1.search(new_str)
				#m2 = comp2.search(new_str)
				for m1 in comp1.findall(new_str):
					print m1.groups()
					seq = m1[0].split()
					start = seq[0]
					s_id = int(start.split("_")[0])
					end = seq[-1]
					e_id = int(end.split("_")[0])
					print " ".join(wlist[s_id-1:e_id])
				print new_str
				for m2 in comp2.findall(new_str):
					
					print m2
					seq = m2[0].split("_")
					if seq[1][:3] != "NNP":
					#seq = m2[1]
						start = m2[1]
						s_id = int(start.split("_")[0])
						print wlist[s_id-1]


				ind = 1
				wlist = []
				taglist = []
			else:
				
				line = line.rstrip()
				l = line.split("\t")
				l[1] = str(ind)+"_"+l[1]
				wlist.append(l[0])
				taglist.append(l[1])
				ind += 1


def byRule(fname):
	## implementation of Extracting company names from text, Lisa Rau 1991
	## Patent title Method for extracting company names from text
	##The program first scans through the input text, looking for company name indicators. If the text is mixed-case, a word must begin with a capital letter in order to be an indicator. The following words are indicators (words prefaced by ABBREV must have periods after them). 

	##______________________________________ ABBREV.sub.-- INC ABBREV.sub.-- LTD ABBREV.sub.-- CORP ABBREV.sub.-- CO ABBREV.sub.-- PLC ABBREV.sub.-- AG ABBREV.sub.-- COS ABBREV.sub.-- LP ABBREV.sub.-- L.P CORP INC LTD CO PLC AG NV CSF SA ABBREV.sub.-- ENTRP ABBREV.sub.-- S.A ABBREV.sub.-- SA ABBREV.sub.-- PTY.LTD ASSOCIATES COMPANY COMPANIES CORPORATION INCORPORATED LIMITED PARTNERS ______________________________________ 
	caps = []
	for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ&":
		caps.append(x)

	indicator=["INC", "LTD", "CORP", "CO", "PLC", "AG", "COS", "LP", "L.P", "N.V", "NV", "CSF", "SA", "ENTRP", "S.A", "PTY.LTD", "ASSOCIATES", "COMPANY", "COMPANIES", "CORPORATION", "INCORPORATED", "LIMITED", "PARTNERS", "INC.", "LTD.", "CORP.", "CO.", "PLC.", "AG.", "COS.", "LP.", "L.P.", "N.V.", "CSF.", "SA.", "ENTRP.", "S.A.", "PTY.LTD.", "ASSOCIATES.", "COMPANY.", "COMPANIES.", "CORPORATION.", "INCORPORATED.", "LIMITED.", "PARTNERS.", "LLC", "LLC."]


	#Additional company name indicators that appear before the final indicator are included as a part of the company name being extracted. One stop condition occurs when the program encounters one of the following words in all-caps input: 

	condition1 = "ABOUT ABOVE ACQUIRE ACQUIRES ACQUIRING AFFILIATE AFFIRMS AFTER AGAINST ALL ALLOW AN APPROVES ARE AS AT BELIEVES BE BEFORE BEGIN BETWEEN BOTH BOUGHT BUY BUYS BY CERTAIN COMPANY COMPLETES CONCERN CONNECT CONTACT COVER DIRECTORS DISTRIBUTE DOWNGRADES EST EVEN EXPECT FILES FOR FORCE FORMER FORMERLY FRIDAY FROM GROUP HAD HAS HAVE HE HELD IN INACTIVE INCLUDE INCLUDES INCLUDING INITIAL INVOLVE INTO IT ITS IS JOINS LEAVING LEFT LONGTIME MAKER MEAN MONDAY NAME NEWSWIRE ON ONE OR OTHER OUT OUTSTANDING OVER OWN OWNS PARENT PARTNER PR PRESIDENT PUBLISHER PURCHASE REQUIRE RESUMED RETAILER SAID SAYS SAY SATURDAY SHOWS SOLD SPLIT STOP SELL SUBSIDIARY SUBSIDIARIES SUNDAY TEXT TO TODAY THAN THAT THE THEIR THREATENING THROUGH THURSDAY TUESDAY UNDER UNIDENTIFIED UNIT UNTIL UPI USE USING USUAL VIA VS WAS WEAKENS WEDNESDAY WERE WHEN WHEREBY WHICH WIRE WITH YESTERDAY JANUARY FEBRUARY MARCH APRIL MAY JUNE JULY AUGYST SEPTEMBER OCTOBER NOVEMBER DECEMBER "
	stopCondition1 = condition1.split() 

	# for the following words, the Company name is assumed to start with the word: 
	
	condition2 = "UNITED APPLIED ALLIED CONSOLIDATED DIVERSIFIED INTEGRATED ADVANCED"
	stopCondition2 = condition2.split()

	#If an AND appears within the six-word window and either there are more than 2 commas within this window, the company name extracted begins with the word after the AND. 

	#If an OF appears within the six-word window and the word directly before the OF is one of the following: 
	#Job titles are added by YHLIN
	condition3 = "BOARD DIVISION OFFICER PROGRAM PROGRAMS DIRECTOR SHAREHOLDERS EXECUTIVE TRADEMARK TRADEMARKS CEO CTO COO CFO PRESIDENT VP"
	stopCondition3 = condition3.split()

	fid = open(fname, "r")
	for lid, s in enumerate(fid):
		#if lid > 20:
		#	break
		#s = s.replace(","," ,")
		ts = s.split()
		for wid, t in enumerate(ts):
			#if wid > 10:
			#	break
			
			#if (t.upper()[:-1] in indicator and t[-1]==".") or t.upper() in indicator:
			if t.upper() in indicator:
				#print t
				stopid = 0
				andId = 0
				i = 0
				commaC = 0
				#for i in range(0,6):
				while i < min(6, wid+1):
					#print ts[wid-i], i
					if ts[wid-i] == "," and ts[wid-i-1].upper() in indicator and ts[wid-i+1].upper() not in indicator:
						stopid = i
						i = 6
						continue
					elif ts[wid-i] == ",":
						commaC += 1
						i += 1
						continue
					#if ts[wid-i][0] not in caps: 
					if re.match(r'[ie]?[A-Z&]', ts[wid-i]) == None: #such as iPad
						
						if ts[wid-i].lower() not in ["and", "du", "van", "de", "of"]:
							stopid = i
							i = 5
						elif ts[wid-i].lower() == "of":
							if ts[wid-i-1].upper() in stopCondition3:
								#print "COND 3"
								stopid = i
								i = 5
						elif ts[wid-i].lower() == "and" and ts[wid-i-1].upper() in indicator:
							stopid = i
							i = 5
						elif ts[wid-i].lower() == "and":
							andId = i
					elif ts[wid-i].upper() in stopCondition1:
						#print "COND 1"
						#stopid = i+1
						stopid = i
						i = 5
					elif ts[wid-i].upper() in stopCondition2:
						#print "COND 2"
						#stopid = i-1
						stopid = i+1
						i = 5
					else:
						#print "COND 4"
						stopid = i+1 # stopped naturally, such as it is from the beginning of the sentence

					i += 1
				#print stopid, i
				if andId < stopid and commaC >= 2:
					stopid = andId+1
				if stopid > 1:
					#print s
					if ts[wid-stopid+1].lower() in ["of", ",", "and"]:
						stopid -= 1
					print str(lid).zfill(4), " ".join(ts[wid-stopid+1:wid+1])
				## look for accronym
				try:
					if ts[wid+1] =="(" and ts[wid+3]==")" and re.search('[^A-Z]', ts[wid+2])==None:
						print "ACCO", ts[wid+2]
				except:
					pass
	fid.close()

if __name__ == "__main__":
	#fname = "ibm_sl/1.txt"
	import sys
	fname = sys.argv[1]
	byRule(fname)
