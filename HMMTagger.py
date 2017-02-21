from nltk import ConditionalProbDist, ConditionalFreqDist, MLEProbDist, bigrams, ngrams
#from nltk.util import ngrams

class HMMTagger(object):
	global START_TAG
	START_TAG = "<s>"
	global END_TAG
	END_TAG = "</s>"

	def __init__(self, tagged_sents, n=4):
		self.n = n
		self.tagged_sents = tagged_sents
		self.train()

	def construct_frequencies(self):
		""" Construct the conditional frequencies and probabilities """
		#extract tags from sentences
		tags = [tag for (_,tag) in self.tagged_sents]
		self.tagset = set(tags)

		self.freqDistTaggedWords = ConditionalFreqDist(self.tagged_sents)
		self.probDistTaggedWords = ConditionalProbDist(self.freqDistTaggedWords, MLEProbDist)

		self.freqDistTags = ConditionalFreqDist(bigrams(tags))
		self.probDistTags = ConditionalProbDist(self.freqDistTags, MLEProbDist)

	def addStartAndEndMarkers(self):
		""" returns a flat list of tokens """
		res = []
		for sent in self.tagged_sents:
			res += [(START_TAG, START_TAG)]
			res += sent
			res += [(END_TAG, END_TAG)]
		self.tagged_sents = res

	def train(self):
		""" Train the model using the training set """
		self.addStartAndEndMarkers()
		self.construct_frequencies()

	def get_start_q(self, word):
		""" The first column of viterbi algorithm """
		start_viterbi = {}
		start_back = {}
		for tag in self.tagset:
			if tag != START_TAG:
				start_viterbi[tag] = self.probDistTags[START_TAG].prob(tag) * self.probDistTaggedWords[word].prob( tag )
				start_back[tag] = START_TAG
		return (start_viterbi, start_back)

	def get_word_viterbi(self, word, prev):
		""" nth column for the viterbi table where n!=0 """
		current_viterbi = {}
		current_back = {}
		for tag in self.tagset:
			if tag != START_TAG:
				best_prev_tag = self.get_prev_tag(tag, prev, word)
				current_viterbi[tag] = prev[best_prev_tag] * self.probDistTags[best_prev_tag].prob(tag) * self.probDistTaggedWords[word].prob( tag )
				current_back[tag] = best_prev_tag
		return (current_viterbi, current_back)


	def viterbi(self, words_to_tag):
		""" Viterbi algorithm """
		res = [] # a list of dicts denoting probability of best path to get to state q after scanning input up to pos i
		back = [] # a list of dicts

		start_viterbi, start_back = self.get_start_q(words_to_tag[0])
		res.append(start_viterbi)
		back.append(start_back)

		for wordindex in range(1, len(words_to_tag)):
			current_viterbi, current_back = self.get_word_viterbi(words_to_tag[wordindex], res[-1])
			res.append(current_viterbi)
			back.append(current_back)

		prev = res[-1]
		back.reverse()
		return self.construct_solution(back, prev)


	def construct_solution(self, back, prev):
		""" Constructs solution by following the back pointers on a ready viterbi table """
		current_best_tag = self.get_prev_tag(END_TAG, prev)
		best_seq = [ END_TAG, current_best_tag ]
		for p in back:
			best_seq.append(p[current_best_tag])
			current_best_tag = p[current_best_tag]
		best_seq.reverse()
		return best_seq

	def get_prev_tag(self, tag, prev, curr_word=None):
		""" Finds a previous tag A for the current tag B s.t. the probability of AB was the highest
		for the current word. """
		# TODO higher order
		best_prev = None
		best_prob = 0.0
		for prevtag in prev.keys():
			# find the maximum probability
			prob = prev[ prevtag ] * self.probDistTags[prevtag].prob(tag)
			if  curr_word:
				prob *= self.probDistTaggedWords[curr_word].prob(tag)
			if prob > best_prob:
				best_prob = prob
				best_prev = prevtag
		if best_prev == None:
			# assign at least something to avoid None exception
			best_prev = prev.keys()[0]
		return best_prev

	def tag(self, test_sents):
		""" Tag the input by combining it first into a list of tokens """
		test_tokens = [j for i in test_sents for j in i]
		return self.viterbi(test_tokens)

	def tag_sents(self, test_sents):
		"""Tag the given text sentence by sentence"""
		res = []
		for sent in test_sents:
			res.append(self.viterbi(sent)[1:-1]) # remove start and end tags
		return res
