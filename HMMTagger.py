from nltk import ConditionalProbDist, ConditionalFreqDist, MLEProbDist, bigrams

class HMMTagger(object):

	def __init__(self, tagged_sents, n=0):
		self.n = n
		self.tagged_sents = tagged_sents

		self.freqDistTaggedWords = ConditionalFreqDist()
		self.construct_freqDist()
		self.probDist = ConditionalProbDist(self.freqDistTaggedWords, MLEProbDist)
		self.freqDistTags= ConditionalFreqDist(bigrams(brown_tags))

	def construct_ngram_freqDist(self):
		""" Conditions are of form (tag, tag, tag, word) """
		for sent in self.tagged_sents:
			history = []
			for token in sent:
				word = token[0]
				tag = token[1]
				context = tuple(history + [word])
				self.freqDistTaggedWords[context][tag] += 1
				history.append(tag)
				if len(history) == (self.n+1):
					del history[0]

	def construct_freqDist(self):
		self.freqDistTaggedWords = ConditionalFreqDist([j for i in self.tagges_sents for j in i])

	def train(self):
		#extract tags from sentences
		tags = []
		for sent in self.tagged_sents:
			tags.extend([t for (_,t) in first])
		# now tags is a list of lists of tags

	def tag(self):
		pass

if __name__ == '__main__':
	from nltk.corpus import brown
	from nltk import ConditionalProbDist, ConditionalFreqDist, MLEProbDist
	sents = brown.tagged_sents()
	#print sents[0]
	hmt = HMMTagger(sents[:2])
	#print hmt.probDist[("irregularities",)].prob("NNS")
