from nltk import ConditionalProbDist, ConditionalFreqDist, MLEProbDist, bigrams

class HMMTagger(object):

	def __init__(self, tagged_sents, n=0):
		self.n = n
		self.tagged_sents = tagged_sents
		self.train()

	def construct_frequencies(self):
		self.construct_freqDistTaggedWords()
		self.probDistTaggedWords = ConditionalProbDist(self.freqDistTaggedWords, MLEProbDist)
		#extract tags from sentences
		tags = []
		for sent in self.tagged_sents:
			tags.extend([t for (_,t) in sent])
		# now tags is a list of tags
		self.freqDistTags = ConditionalFreqDist(bigrams(tags))
		# TODO change from bigrams to ngrams
		self.probDistTags = ConditionalProbDist(self.freqDistTags, MLEProbDist)

	def construct_ngram_freqDist(self):
		""" Conditions are of form (tag, tag, tag, word) """
		self.freqDistTaggedWords = ConditionalFreqDist()
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

	def construct_freqDistTaggedWords(self):
		self.freqDistTaggedWords = ConditionalFreqDist([j for i in self.tagged_sents for j in i])

	def train(self):
		self.construct_frequencies()
		

	def tag(self):
		pass

if __name__ == '__main__':
	from nltk.corpus import brown
	from nltk import ConditionalProbDist, ConditionalFreqDist, MLEProbDist
	sents = brown.tagged_sents()
	print sents
	hmt = HMMTagger(sents[:2])
	#print hmt.probDist[("irregularities",)].prob("NNS")
