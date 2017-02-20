from nltk import ConditionalProbDist, ConditionalFreqDist, MLEProbDist, bigrams, ngrams

class HMMTagger(object):
	global START_TAG
	START_TAG = "<s>"
	global END_TAG
	END_TAG = "</s>"

	def __init__(self, tagged_sents, n=0):
		self.n = n
		self.tagged_sents = tagged_sents
		self.train()

	def construct_frequencies(self):
		self.construct_freqDistTaggedWords()
		self.probDistTaggedWords = ConditionalProbDist(self.freqDistTaggedWords, MLEProbDist)
		#extract tags from sentences
		tags = []
		# V1 - for list of sentences
		#for sent in self.tagged_sents:
		#	tags.extend([t for (_,t) in sent])

		# V2 - for list of words
		for (word, tag) in self.tagged_sents:
			tags += [tag]
		self.tagset = set(tags)
		# now tags is a list of tags
		self.freqDistTags = ConditionalFreqDist(bigrams(tags))
		# TODO change from bigrams to ngrams
		self.probDistTags = ConditionalProbDist(self.freqDistTags, MLEProbDist)

	def construct_ngram_freqDist(self):
		""" Conditions are of form (tag, ..., tag, word) """
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
		#""" for tagged_sents that are a list of lists """
		#self.freqDistTaggedWords = ConditionalFreqDist([j for i in self.tagged_sents for j in i])
		# for tagged_sents that are already joined
		self.freqDistTaggedWords = ConditionalFreqDist(self.tagged_sents)

	def addStartAndEndMarkers(self):
		""" returns a flat list of tokens """
		res = []
		for sent in self.tagged_sents:
			res += [(START_TAG, START_TAG)]
			res += sent
			res += [(END_TAG, END_TAG)]
		self.tagged_sents = res

	def train(self):
		self.addStartAndEndMarkers()
		self.construct_frequencies()


	def viterbi(self, words_to_tag):
		res = [] # a 2D matrix denoting probability of best path to get to state q after scanning input up to pos i
		back = [] # a 2D matrix
		start_viterbi = {}
		start_back = {}
		for tag in self.tagset:
			if tag != START_TAG:
				start_viterbi[tag] = self.probDistTags[START_TAG].prob(tag) * self.probDistTaggedWords[words_to_tag[0]].prob( tag )
				start_back[tag] = START_TAG
		res.append(start_viterbi)
		back.append(start_back)
		print start_viterbi
		print start_back

	def tag(self, test_tokens):
		return self.viterbi(test_tokens)

if __name__ == '__main__':
	from nltk.corpus import brown
	from nltk import ConditionalProbDist, ConditionalFreqDist, MLEProbDist
	sents = brown.tagged_sents()
	hmt = HMMTagger(sents[:10])
	print hmt.probDistTaggedWords.conditions()[:4]
	print hmt.probDistTaggedWords["irregularities"].prob("NNS")
	hmt.tag(["The", "Fulton", "county"])
