#coding: utf-8
'''
Takes a list of files, parses them as TXT or XML, extracts all words and finds
out how many of these words match German dictinary.

The purpose is to estimate the OCR engine quality when processing different
types of documents in German.

@author: mkroutikov
'''
import io
import os
import re
import glob
import collections
import csv

def parse_corpus(fname):

    corpus = []
    with io.open('dictionary/german.dic', 'r', encoding='cp1252') as f:
        for word in f:
            word = word.strip()
            if not word:
                continue
            corpus.append(word)

    return corpus

def stats_txt(fname, dictionary):

    with io.open(fname, 'r', encoding='utf-8') as f:
        text = f.read()

    per_file = collections.defaultdict(int)
    for word in re.findall(r'\w+', text):
        word = word.lower()

        if re.match(r'\d+$', word):
            per_file['numeric'] += 1
        elif len(word) < 3:
            per_file['short'] += 1
        elif word in dictionary:
            per_file['dictionary'] += 1
        else:
            per_file['non-dictionary'] += 1
        per_file['total'] += 1

    return per_file

def merge(d1, *av):
    '''merge one or more dictionaries into the first one'''
    for d in av:
        d1.update(d)
    return d1

def file_stats_txt(glob_pattern, dictionary, output_fname):

    totals = collections.defaultdict(int)
    with io.open(output_fname, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'numeric', 'short', 'dictionary', 'non-dictionary', 'total'])
        writer.writeheader()

        for fname in sorted(glob.glob(glob_pattern)):
            name = os.path.basename(fname)
            print('Processing:', name)

            per_file = stats_txt(fname, dictionary)

            for key, val in per_file.items():
                totals[key] += val

            writer.writerow(merge({
                'name': name
            }, per_file))

        writer.writerow(merge({
            'name': 'Totals'
        }, totals))

if __name__ == '__main__':

    print('Loading German dictionary...')
    corpus = parse_corpus('dictionary/german.dic')

    dictionary = set(x.lower() for x in corpus)
    print('Loaded', len(dictionary), 'unique lowercase words')

    file_stats_txt('ocr-hlsl/*.txt', dictionary, output_fname='ocr-hlsl.csv')
