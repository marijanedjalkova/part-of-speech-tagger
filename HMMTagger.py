class HMMTagger(object):

    def __init__(self, n=2):
        self.n = n

    def tag(self, testing_tokens):
        return []

    def train(self, training_tokens):
        history = []

        for token in training_tokens:
            context = tuple(history,  + [])
