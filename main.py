from nltk.corpus import brown

def show_sent(sent):
    print sent



def main():
    sents = brown.tagged_sents()
    # 57340 sentences
    training_set = sents[:50000]
    testing_set = sents[50000:50500]
    

if __name__ == '__main__':
    main()
