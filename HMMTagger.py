from nltk import FreqDist, ConditionalProbDist, ConditionalFreqDist, MLEProbDist, bigrams, ngrams
import time

class HMMTagger(object):
	global START_TAG
	START_TAG = "<s>"
	global END_TAG
	END_TAG = "</s>"
	global UNK
	UNK = "UNK"

	def __init__(self, training_sents, n=2):
		self.n = n
		self.tagged_sents = self.addStartAndEndMarkers(training_sents)
		self.train()

	def train(self):
		""" Construct the conditional frequencies and probabilities """
		#extract tags from sentences
		tags = [tag for (_,tag) in self.tagged_sents]
		self.tagset = set(tags)

		self.replaceUnique()

		self.emission_frequencies = ConditionalFreqDist([tup[::-1] for tup in self.tagged_sents])

		# emission - probability that a certain tag is a certain word
		# e.g. probability that a VB is 'race'
		self.emission_probabilities = ConditionalProbDist(self.emission_frequencies, MLEProbDist)

		self.transition_frequencies = ConditionalFreqDist(bigrams(tags)) # TODO change to ngrams
		self.transition_probabilities = ConditionalProbDist(self.transition_frequencies, MLEProbDist)

		print "Model trained."

	def replaceUnique(self):
		""" Replaces unique words with the UNK label """
		start = time.time()
		word_frequencies = FreqDist([word for (word, _) in self.tagged_sents])
		hap = set(word_frequencies.hapaxes())
		res = [(UNK,tag) if word in hap else (word,tag) for (word,tag) in self.tagged_sents]
		self.tagged_sents = res
		counter = 0

	def addStartAndEndMarkers(self, training_sents):
		""" returns a flat list of tokens """
		res = []
		for sent in training_sents:
			res += [(START_TAG, START_TAG)]
			res += sent
			res += [(END_TAG, END_TAG)]
		return res


	def viterbi_col(self, word, prev=None):
		""" General algorithm for a viterbi table column.
		This is only called once for every word. """
		vit = {}
		back = {}

		for tag in self.tagset:
			if tag != START_TAG:
				if prev:

					best_prev_tag = self.get_prev_tag(tag, prev, word)
					vit[tag] = prev[best_prev_tag] * self.transition_probabilities[best_prev_tag].prob(tag) * self.emission_probabilities[ tag ].prob( word )
					back[tag] = best_prev_tag

				else:
					vit[tag] = self.transition_probabilities[START_TAG].prob(tag) * self.emission_probabilities[ tag ].prob( word )
					back[tag] = START_TAG

		return (vit, back)


	def viterbi(self, words_to_tag):
		""" Viterbi algorithm """
		res = [] # a list of dicts denoting probability of best path to get to state q after scanning input up to pos i
		backpointers = [] # a list of dicts

		for wordindex in range(len(words_to_tag)):
			current_word = words_to_tag[wordindex]
			if self.is_unknown(current_word):
				current_word = UNK
			if wordindex == 0:
				vit, back = self.viterbi_col(current_word)
			else:
				vit, back = self.viterbi_col(current_word, res[-1])

			res.append(vit)
			backpointers.append(back)

		prev = res[-1]
		backpointers.reverse()
		return self.construct_solution(backpointers, prev)

	def is_unknown(self, word):
		""" Checks if the word is unknown """
		for tag in set(self.emission_probabilities.conditions()):
			pr = self.emission_probabilities[tag]
			if pr.prob( word ) > 0:
				return False
		return True

	def construct_solution(self, back, prev):
		""" Constructs solution by following the back pointers on a ready viterbi table """
		current_best_tag = self.get_prev_tag(END_TAG, prev)

		best_seq = [ END_TAG, current_best_tag ]
		for p in back:
			to_append = p[current_best_tag]
			best_seq.append(to_append)
			current_best_tag = p[current_best_tag]
		best_seq.reverse()
		return best_seq

	def get_prev_tag(self, tag, prev, curr_word=None):
		""" Finds a previous tag A for the current tag B s.t. the probability of AB was the highest
		for the current word.
		Called for every word and every tag """
		# TODO higher order
		best_prev = None
		best_prob = 0.0

		for prevtag in prev.keys():
			# find the maximum probability
			prob = prev[ prevtag ] * self.transition_probabilities[prevtag].prob(tag)

			if  curr_word:
				prob *= self.emission_probabilities[ tag ].prob( curr_word )

			if prob > best_prob:
				best_prob = prob
				best_prev = prevtag

		if best_prev == None:
			# assign at least something to avoid None exception
			best_prev = prev.keys()[0]
		return best_prev

	def tag_sents(self, test_sents):
		"""Tag the given text sentence by sentence"""
		res = []
		for sent in test_sents:
			res.append(self.viterbi(sent)[1:-1])# remove start and end tags
		return res
