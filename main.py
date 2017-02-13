from nltk.corpus import brown
from HMMTagger import HMMTagger
from nltk.tokenize import word_tokenize

def show_sent(sent):
    print sent

def main():
    sents = brown.tagged_sents()
    # 57340 sentences
    training_set = sents[:50000]
    testing_set = sents[50000:50002]
    t = HMMTagger(3)
    t.train(training_set)
    test_words = [[w for (w,_) in sentence] for sentence in testing_set]
    test_tags = [[tag for (_,tag) in sentence] for sentence in testing_set]
    new_tags = t.tag(test_words)
    print compare(new_tags, test_tags), "%"


def compare(detected_tags_lst, original_tags_lst):
    res = 0
    total = 0;
    for detected_sent, original_sent in zip(detected_tags_lst, original_tags_lst):
        for detected, original in zip(detected_sent, original_sent):
            total +=1
            if detected == original:
                res+=1
    return (res*100.0)/(total*1.0)


if __name__ == '__main__':
    main()
