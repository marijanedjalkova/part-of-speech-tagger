from nltk.corpus import brown
from HMMTagger import HMMTagger
from NGramTagger import NGramTagger
from nltk.tokenize import word_tokenize

def main():
    sents_to_plain()
    return
    sents = brown.tagged_sents()
    # 57340 sentences
    training_set = sents[:50000]
    testing_set = sents[50000:50002]

    t = HMMTagger(training_set)
    test_words = [[w for (w,_) in sentence] for sentence in testing_set]
    test_tag_sents = [[tag for (_,tag) in sentence] for sentence in testing_set]
    #test_tags = [j for i in test_tag_sents for j in i]
    new_tags = t.tag(test_words)
    print compare(new_tags, test_tags), "%"

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

def sents_to_plain():
    sents = [[u'BEDZ-NC', u'BEDZ-NC', u'BEDZ-NC'], [u'BEDZ-NC', u'BEDZ-NC', u'BEDZ-NC', u'BEDZ-NC']]
    res = []
    for s in sents:
        res.append("<s>")
        res.extend(s)
        res.append("</s>")
    return res


def compare(detected_tags_lst, original_tags_lst):
    res = 0
    total = 0
    for detected_sent, original_sent in zip(detected_tags_lst, original_tags_lst):
        for detected, original in zip(detected_sent, original_sent):
            total +=1
            if detected == original:
                res+=1
    return (res*100.0)/(total*1.0)


if __name__ == '__main__':
    main()
