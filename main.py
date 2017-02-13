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
import lxml.etree as et

def parse_corpus(fname):

    corpus = []
    with io.open('dictionary/german.dic', 'r', encoding='cp1252') as f:
        for word in f:
            word = word.strip()
            if not word:
                continue
            corpus.append(word)

    return corpus

def words_from_txt(fname):
    with io.open(fname, 'r', encoding='utf-8') as f:
        text = f.read()

    yield from re.findall(r'\w+', text)

def words_from_xml(fname):
    with io.open(fname, 'rb') as f:
        xml = et.fromstring(f.read())

    for elt in xml.findall('.//word'):
        text = elt.attrib['text']

        yield from re.findall(r'\w+', text)

def stats(dictionary, words):

    per_file = collections.defaultdict(int)
    for word in words:
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

            per_file = stats(dictionary, words_from_txt(fname))

            for key, val in per_file.items():
                totals[key] += val

            writer.writerow(merge({
                'name': name
            }, per_file))

        writer.writerow(merge({
            'name': 'Totals'
        }, totals))

def file_stats(files, dictionary, output_fname):

    totals = collections.defaultdict(int)
    with io.open(output_fname, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'numeric', 'short', 'dictionary', 'non-dictionary', 'total'])
        writer.writeheader()

        for name, words in files:
            print('Processing:', name)

            per_file = stats(dictionary, words)

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

    def txt_files():
        for fname in glob.glob('ocr-hlsl/*.txt'):
            yield os.path.basename(fname), words_from_txt(fname)

    def xml_files():
        for fname in glob.glob('ocr-inno/*.xml'):
            yield os.path.basename(fname), words_from_xml(fname)

    file_stats(txt_files(), dictionary, output_fname='ocr-hlsl.csv')
    file_stats(xml_files(), dictionary, output_fname='ocr-inno.csv')
