from nltk import ConditionalFreqDist

class HMMTagger(object):

    def __init__(self, n=2):
        self.n = n
        self.freqDist = ConditionalFreqDist()

    def tag(self, testing_tokens):
        return []

    def train(self, training_sents):
        history = []
        for sent in training_sents:
            for token in sent:
                context = tuple(history + [token[0]])
                feature = token[1]
                self.freqDist[context][feature] += 1
                history.append(token[1])
                if len(history) == (self.n+1):
                    del history[0]

    def next_tag(self, tagged_tokens, next_token):
        context = tuple(tagged_tokens + [next_token])
        return self.freqDist[context].max()
