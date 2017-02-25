from nltk.corpus import brown
from HMMTagger import *
import sys, getopt
import time

smoothing = "LAP"
trainstart = 0
trainlength = 5000
testlength = 2

def process_args(argv, num_of_sents):
    global smoothing, trainstart, trainlength, testlength
    try:
        opts, args = getopt.getopt(argv, "s:t:l:e:",["smoothing=", "trainstart=", "trainlength=", "testing="])
    except getopt.GetoptError:
        print 'Could not get arguments'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-s', '--smoothing'):
            smoothing = arg
        elif opt in ('-t', '--trainstart'):
            if not (arg.isdigit() and (0 <= int(arg) <= (num_of_sents - 1))):
                print "wrong argument type for ", opt, ", will use default value "
                continue
            trainstart = int(arg)
        elif opt in ('-l', '--trainlength'):
            if not (arg.isdigit() and (0 <= int(trainstart) + int(arg) <= num_of_sents - 5)):
                print "wrong argument type for ", opt, ", will use default value "
                continue
            trainlength = int(arg)
        elif opt in ('-e', '--testing'):
            if not (arg.isdigit() and (0 <= int(trainstart) + int(trainlength) + int(arg) <= num_of_sents)):
                print "wrong argument type for ", opt, ", will use default value "
                continue
            testlength = int(arg)
        else:
            continue

def merge(sents, merging):
    new_sents = []
    for sent in sents:
        new_sent = []
        for (w,t) in sent:
            new_tuple = (w,t)
            if "+" in merging and "+" in t:
                new_tuple = (w, t.split("+")[0])
            for m in merging:
                if t.startswith(m):
                    new_tuple = (w,m)
                    break
            new_sent.append(new_tuple)
        new_sents.append(new_sent)
    return new_sents

def process_data(sents, merging):
    """Merge and split data into different sets.
    Return training set, testing words and testing tags."""
    merged_sents = merge(sents, merging)
    training_set = merged_sents[ trainstart : trainstart + trainlength ]
    testing_set = merged_sents[ trainstart + trainlength + 1 : trainstart + trainlength + 1 + testlength ]
    test_words = [[meow for (meow,_) in sentence] for sentence in testing_set]
    test_tag_sents = [[tag for (_,tag) in sentence] for sentence in testing_set]
    return (training_set, test_words, test_tag_sents)


def main(argv):
    sents = brown.tagged_sents()
    num_of_sents = 57340
    # I know this is a magic number but len(sents) takes too long.
    process_args(argv, num_of_sents)
    training_set, test_words, test_tag_sents = process_data(sents, ("BE", "NN", "JJ", "DT", "FW", "HV", "MD", "NP", "VB", "WDT", "WPS", "WRB", "+"))
    t = HMMTagger(training_set, smoothing=smoothing)
    print t.tagset
    new_tag_sents = t.tag_sents(test_words)
    #print new_tag_sents
    print "all merging: ", compare(new_tag_sents, test_tag_sents), "%"
    print "Accuracy for nouns: ", measure_accuracy_for_class(new_tag_sents, test_tag_sents, "NN"), "%"
    print "Accuracy for adjectives: ", measure_accuracy_for_class(new_tag_sents, test_tag_sents, "JJ"), "%"

    training_set, test_words, test_tag_sents = process_data(sents, ())
    t = HMMTagger(training_set, smoothing=smoothing)
    new_tag_sents = t.tag_sents(test_words)
    #print new_tag_sents
    print "No merging: ", compare(new_tag_sents, test_tag_sents), "%"
    print "Accuracy for nouns: ", measure_accuracy_for_class(new_tag_sents, test_tag_sents, "NN"), "%"
    print "Accuracy for adjectives: ", measure_accuracy_for_class(new_tag_sents, test_tag_sents, "JJ"), "%"


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
    for detected, original in zip(detected_tags_lst, original_tags_lst):
        total +=1
        if detected == original:
            res+=1
    if total == 0:
        print "no occurrences!"
        return 1

    return (res*100.0)/(total*1.0)

def measure_accuracy_for_class(detected_tags_sents, original_tags_sents, tag_class):
    res = 0
    total = 0
    original_tags_lst = sents_to_plain(original_tags_sents)
    detected_tags_lst = sents_to_plain(detected_tags_sents)
    for detected, original in zip(detected_tags_lst, original_tags_lst):
        if original==tag_class:
            total +=1
            if detected == original:
                res+=1
    return (res*100.0)/(total*1.0)


if __name__ == '__main__':
    main(sys.argv[1:])
