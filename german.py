#coding: utf-8
import io
import re
import pickle


def parse_corpus(fname):

    corpus = []
    with io.open('dictionary/german.dic', 'r', encoding='cp1252') as f:
        for word in f:
            word = word.strip()
            if not word:
                continue
            corpus.append(word)

    return corpus

def save_corpus(corpus):

    with io.open('corpus.pickle', 'wb') as f:
        pickle.dump(corpus, f, pickle.HIGHEST_PROTOCOL)

def load_corpus():

    with io.open('corpus.pickle', 'rb') as f:
        return pickle.load(f)

def search_corpus(corpus, regex):
    for word in corpus:
        if re.match(regex, word, re.IGNORECASE):
            yield word


if __name__ == '__main__x':

    corpus = parse_corpus('data/german.dic')
    print('loaded corpus of', len(corpus), 'words')

    save_corpus(corpus)

if __name__ == '__main__':

    corpus = load_corpus()
    print('unpickled corpus of', len(corpus), 'words')

    for word in search_corpus(corpus, r'...?(m|n)g(f|t)en$'):
        print(word)

'''
Solgen:
'''
