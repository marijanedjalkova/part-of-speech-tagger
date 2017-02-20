from nltk import ConditionalFreqDist

class NGramTagger(object):
    """ N-Gram Part-of-Speech tagger """

    def __init__(self, n=0):
        """ Constructor.
        n - the number of previous tags considered
        freqDist - a condiditional frequency distribution """
        self.n = n
        self.freqDist = ConditionalFreqDist()

    def train(self, training_sents):
        """ Trains the model by remembering the existing patterns of length n """
        for sent in training_sents:
            history = []
            for token in sent:
                word = token[0]
                tag = token[1]
                context = tuple(history + [word])
                self.freqDist[context][tag] += 1
                history.append(tag)
                if len(history) == (self.n+1):
                    del history[0]

    def next_tag(self, tagged_tokens, next_token):
        """ Determins the POS tag for the next_token based on the given
        tagged_tokens. Returns the tag """
        context = tuple(tagged_tokens + [next_token])
        print "context ", context
        if context in self.freqDist:
            return self.freqDist[context].max()
        else:
            return "UNK"

    def tag(self, tokenized_sents):
        """ Tags the given set of tokenized sentences. Returns a list of lists of tags. """
        res = []
        for sentence in tokenized_sents:
            tagged_sentence = []
            for token in sentence:
                context = tagged_sentence[-self.n:]
                tagged_sentence.append(self.next_tag(context, token))
            res.append(tagged_sentence)
        return res
