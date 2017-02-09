from nltk import ConditionalFreqDist

class HMMTagger(object):

    def __init__(self, n=2):
        self.n = n
        self.freqDist = ConditionalFreqDist()

    def tag(self, tokens):
        res = []
        for token in tokens:
            context = res[-self.n:]
            print "--context ", context
            res.append(self.next_tag(context, token))
        return res

    def train(self, training_sents):
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
        context = tuple(tagged_tokens + [next_token])
        if context in self.freqDist:
            return self.freqDist[context].max()
        else:
            return None
