class HMMTagger(object):

    def __init__(self, n=2):
        self.n = n
        self.freqDist = CFFreqDist()

    def tag(self, testing_tokens):
        return []

    def train(self, training_tokens):
        history = []

        for token in training_tokens:
            context = tuple(history + [token[0]])
            feature = token[1]
            self.freqDist[context].inc(feature)
            history.append(token[1])
            if len(history) == (self.n+1):
                del history[0]

    def next_tag(self, tagged_tokens, next_token):
        # Find the tags of the n previous tokens.
        history = []
        start = max(len(tagged_tokens) - self.n, 0)
        for token in tagged_tokens[start:]:
            history.append(token[1])
            # Return the most likely tag for the token’s context.
            context = tuple(history + [next_token.type()])
            return self.freqDist[context].max()
