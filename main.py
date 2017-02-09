from nltk.corpus import brown
from HMMTagger import HMMTagger

def show_sent(sent):
    print sent

def main():
    sents = brown.tagged_sents()
    # 57340 sentences
    training_set = sents[:50000]
    testing_set = sents[50000:50500]
    t = HMMTagger()
    t.train(training_set)
    print t.next_tag(['VBD', 'NN'], ".")



def compare(detected_tags_lst, original_tags_lst):
    return (sum([1 if x == y else 0 for x, y in zip(detected_tags, original_tags)]), len(original_tags))

if __name__ == '__main__':
    main()
