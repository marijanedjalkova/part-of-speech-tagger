from nltk.corpus import brown
from HMMTagger import *
from NGramTagger import NGramTagger
from nltk.tokenize import word_tokenize
import sys, getopt
import numbers
import time


def main(argv):
    smoothing = "LAP"
    trainstart = 0
    trainlength = 5000

    sents = brown.tagged_sents()
    num_of_sents = len(sents)
    # 57340 sentences

    try:
        opts, args = getopt.getopt(argv, "s:t:l:",["smoothing=", "trainstart=", "trainlength="])
    except getopt.GetoptError:
        print 'Could not get arguments'
        sys.exit(2)
    for opt, arg in opts:
        print arg
        if opt in ('-s', '--smoothing'):
            smoothing = arg
            continue
        if opt in ('-t', '--trainstart'):
            if not (arg.isdigit() and (0 <= int(arg) <= (num_of_sents - 1))):
                print "wrong argument type for ", opt, ", will use default value "
                continue
            trainstart = int(arg)
            continue
        if opt in ('-l', '--trainlength'):
            if not (arg.isdigit() and (0 <= int(trainstart) + int(arg) <= num_of_sents)):
                print "wrong argument type for ", opt, ", will use default value "
                continue
            trainlength = int(arg)

    training_set = sents[:50000]
    testing_set = sents[50001:50003]
    t = HMMTagger(training_set, smoothing=smoothing)

    test_words = [[meow for (meow,_) in sentence] for sentence in testing_set]
    test_tag_sents = [[tag for (_,tag) in sentence] for sentence in testing_set]

    new_tag_sents = t.tag_sents(test_words)
    print compare(new_tag_sents, test_tag_sents), "%"

def plain_to_sents(tags):
    """ Parses a list of tags where sentences are separated by start and end tags into list of lists"""
    res = []
    small = []
    for t in tags:
        if t==START_TAG:
            continue
        if t==END_TAG:
            res.append(small)
            small = []
            continue
        small.append(t)
    return res

def sents_to_plain(sents):
    """ Jois a list of lists into a plain list """
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
    main(sys.argv[1:])
