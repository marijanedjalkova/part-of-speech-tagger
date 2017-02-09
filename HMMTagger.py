from nltk import ConditionalFreqDist

class HMMTagger(object):

    def __init__(self, n=2):
        self.n = n
        self.freqDist = ConditionalFreqDist()

    def tag(self, tokens):
        res = []
        for token in tokens:
            context = res[-self.n:]
            res.append(self.next_tag(context, token))
        return res

    def train(self, training_sents):
        history = []
        for sent in training_sents:
            for token in sent:
                word = token[0]
                tag = token[1]
                context = tuple(history + [word])
                self.freqDist[context][tag] += 1
                history.append(tag)
                if len(history) == (self.n+1):
                    del history[0]
        print self.freqDist.conditions()

    def next_tag(self, tagged_tokens, next_token):
        context = tuple(tagged_tokens + [next_token])
        return self.freqDist[context].max()
