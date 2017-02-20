from nltk.corpus import brown
from HMMTagger import HMMTagger
from NGramTagger import NGramTagger
from nltk.tokenize import word_tokenize

def main():
    sents = brown.tagged_sents()
    # 57340 sentences
    training_set = sents[:50000]
    testing_set = sents[:2]
    t = HMMTagger(training_set)
    test_words = [[w for (w,_) in sentence] for sentence in testing_set]
    test_tag_sents = [[tag for (_,tag) in sentence] for sentence in testing_set]
    new_tag_sents = t.tag_sents(test_words)
    print compare(new_tag_sents, test_tag_sents), "%"

def plain_to_sents(tags):
    res = []
    small = []
    for t in tags:
        if t=="<s>":
            continue
        if t=="</s>":
            res.append(small)
            small = []
            continue
        small.append(t)
    return res

def sents_to_plain(sents):
    return [j for i in sents for j in i]


def compare(detected_tags_sents, original_tags_sents):
    res = 0
    total = 0
    original_tags_lst = sents_to_plain(original_tags_sents)
    detected_tags_lst = sents_to_plain(detected_tags_sents)
    print "detected: ", detected_tags_lst
    print "original: ", original_tags_lst
    for detected, original in zip(detected_tags_lst, original_tags_lst):
        total +=1
        if detected == original:
            res+=1
    return (res*100.0)/(total*1.0)


if __name__ == '__main__':
    main()
