#Rough implementation of LESKWSD
#2016.06.14
#reference might be: /cygdrive/c/Users/yhlin/Downloads/REpapers/pywsd-master

from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw

stopword = sw.words("english")
preps = ["above", "along", "at", "below", "beside", "between", "during", "for", "from", "in", "near", "on", "outside", "over"
,"past", "through", "towards", "under", "up", "with", "of", "what", "where", "who", "how", "when", "why"]


def LeskWSD(question, headword, debug = 0):
	content_word = question.split()

	count = 0
	maxCount = -1
	senseOptimal = None

	syns = wn.synsets(headword)
	for syn in syns:
		count = 0
		sd = syn.definition
		sdlist = set(sd.split())

		for c in content_word:
			if (c in stopword) or (c in preps) or c == headword:
				continue
			submax = 0
			for s in wn.synsets(c):
				if syn == s:
					continue
				ssd = s.definition
				ssdlist = set(ssd.split())
				common = sdlist & ssdlist - set(stopword)
				if debug:
					print syn, s, common
				if len(common) > submax:
					submax = len(common)
					subcommon = common
			count += submax
		if count > maxCount:
			maxCount = count
			senseOptimal = syn

	print "Sense optimal is:", senseOptimal

if __name__ == "__main__":
	"""
	sample input: sentence and its head, which can be extracted by getQuestionHead.py
	What is the capital of Taiwan, capital
	What are the landmarks of capital in Taiwan, landmarks
	"""
	LeskWSD("What is the capital of Taiwan", "capital", 1)

