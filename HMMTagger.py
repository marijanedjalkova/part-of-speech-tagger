from nltk import ConditionalProbDist, ConditionalFreqDist, MLEProbDist, bigrams, ngrams
#from nltk.util import ngrams

class HMMTagger(object):
	global START_TAG
	START_TAG = "<s>"
	global END_TAG
	END_TAG = "</s>"

	def __init__(self, tagged_sents, n=2):
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
		self.freqDistTags = ConditionalFreqDist(ngrams(tags, self.n))
		# TODO change from bigrams to ngrams
		self.probDistTags = ConditionalProbDist(self.freqDistTags, MLEProbDist)

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
		res = [] # a list of dicts denoting probability of best path to get to state q after scanning input up to pos i
		back = [] # a list of dicts
		start_viterbi = {}
		start_back = {}
		for tag in self.tagset:
			if tag != START_TAG:
				start_viterbi[tag] = self.probDistTags[START_TAG].prob(tag) * self.probDistTaggedWords[words_to_tag[0]].prob( tag )
				start_back[tag] = START_TAG
		res.append(start_viterbi)
		back.append(start_back)

		for wordindex in range(1, len(words_to_tag)):
			current_viterbi = {}
			current_back = {}
			prev = res[-1]
			for tag in self.tagset:
				if tag != START_TAG:
					best_prev_tag = self.get_prev_tag(tag, prev, words_to_tag[wordindex])
					current_viterbi[tag] = prev[best_prev_tag] * self.probDistTags[best_prev_tag].prob(tag) * self.probDistTaggedWords[words_to_tag[wordindex]].prob( tag )
					current_back[tag] = best_prev_tag

			res.append(current_viterbi)
			back.append(current_back)

		prev = res[-1]
		best_prev_tag = self.get_prev_tag(END_TAG, prev)
		prob_seq = prev[ best_prev_tag ] * self.probDistTags[ best_prev_tag].prob(END_TAG)
		best_seq = [ END_TAG, best_prev_tag ]
		back.reverse()
		current_best_tag = best_prev_tag
		for p in back:
			best_seq.append(p[current_best_tag])
			current_best_tag = p[current_best_tag]
		best_seq.reverse()
		return best_seq

	def get_prev_tag(self, tag, prev, curr_word=None):
		best_prev = None
		best_prob = 0.0
		for prevtag in prev.keys():
			if not curr_word:
				prob = prev[ prevtag ] * self.probDistTags[prevtag].prob(tag)
			else:
				prob = prev[ prevtag ] * self.probDistTags[prevtag].prob(tag) * self.probDistTaggedWords[curr_word].prob(tag)
			if prob > best_prob:
				best_prob = prob
				best_prev = prevtag
		if best_prev == None:
			best_prev = prev.keys()[0]
		return best_prev

	def tag(self, test_sents):
		test_tokens = [j for i in test_sents for j in i]
		return self.viterbi(test_tokens)

	def tag_sents(self, test_sents):
		res = []
		for sent in test_sents:
			print " sent is ", sent
			res.append(self.viterbi(sent)[1:-1]) # remove start and end tags
		return res


if __name__ == '__main__':
	from nltk.corpus import brown
	from nltk import ConditionalProbDist, ConditionalFreqDist, MLEProbDist
	sents = brown.tagged_sents()
	hmt = HMMTagger(sents[:20000])
	hmt.tag(["The", "Fulton", "county"])
