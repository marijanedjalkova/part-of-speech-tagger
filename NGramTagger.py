from nltk import ConditionalFreqDist, FreqDist

class NGramTagger(object):
	global START_TAG
	START_TAG = "<s>"
	global END_TAG
	END_TAG = "</s>"
	global UNK
	UNK = "UNK"

	def __init__(self, training_sents, n=2):
		self.n = n
		self.freqDist = ConditionalFreqDist()
		self.tagged_sents = self.addStartAndEndMarkers(training_sents)
		self.train()

	def addStartAndEndMarkers(self, training_sents):
		""" returns a flat list of tokens """
		res = []
		for sent in training_sents:
			res += [(START_TAG, START_TAG)]
			res += sent
			res += [(END_TAG, END_TAG)]
		return res

	def replaceUnique(self):
		""" Replaces unique words with the UNK label """
		word_frequencies = FreqDist([word for (word, _) in self.tagged_sents])
		self.lexicon_size = len(word_frequencies)
		hap = set(word_frequencies.hapaxes())
		res = [(UNK,tag) if word in hap else (word,tag) for (word,tag) in self.tagged_sents]
		self.tagged_sents = res

	def train(self):
		""" Trains the model by remembering the existing patterns of length n """
		self.replaceUnique()
		history = []
		for (word, tag) in self.tagged_sents:
			context = tuple(history + [word])
			self.freqDist[context][tag] += 1
			history.append(tag)
			if len(history) == (self.n+1):
				del history[0]

	def next_tag(self, tagged_tokens, next_token):
		""" Determins the POS tag for the next_token based on the given
		tagged_tokens. Returns the tag """
		context = tuple(tagged_tokens + [next_token])
		if context in self.freqDist:
			return self.freqDist[context].max()
		else:
			return "UNK"

	def tag_sents(self, tokenized_sents):
		""" Tags the given set of tokenized sentences. Returns a list of lists of tags. """
		res = []
		for sentence in tokenized_sents:
			tagged_sentence = []
			for token in sentence:
				context = tagged_sentence[-self.n:]
				tagged_sentence.append(self.next_tag(context, token))
			res.append(tagged_sentence)
		return res
