#!/usr/local/bin/python
# coding: utf-8

import codecs
import pymorphy2
import sys

# Load input file, return all words
def load_text(fname):
    words = {}
    input_file = codecs.open(fname, 'r', 'utf-8')
    for line in input_file:
        cur = line.split()
        for i in range(len(cur)):
            cur[i] = cur[i].strip('.,:;!?-~[]()')
            words[cur[i]] = line.rstrip()
    print 'Obtained list of words.'
    return words

# Lemmatize the words
def lemmatize(words):
    lemmas = {}
    morph = pymorphy2.MorphAnalyzer()
    for word in words.keys():
        parse = morph.parse(word)[0]
        res = parse.normal_form
        if res not in lemmas.keys():
            lemmas[res] = [1, [words[word]]]
        else:
            lemmas[res][0] += 1
            lemmas[res][1].append(words[word])
    print 'Words are lemmatized.'
    return lemmas

# Find POS and frequency
def find_pos_freq(lemma, dict):
    possible_pos_freq = {}
    possible_pos_freq[lemma] = []
    for line in dict:
        if lemma == line.split('\t')[0]:
            possible_pos_freq[lemma].append((line.split('\t')[1], line.split('\t')[2]))
    return possible_pos_freq[lemma]

# Make a table with lemma-amount-POS-frequency
def create_table(dict_fname, out_fname, lemmas, version):
    print 'Creating table...'
    chosen_pos_freq = {}
    dict = []
    f_dict = codecs.open(dict_fname, 'r', 'utf-8')
    for line in f_dict:
        dict.append(line)
    table = codecs.open(out_fname, 'w', 'utf-8')
    table.write(u'Лемма\tКоличество вхождений\tPOS\tЧастотность\n')
    for lemma in lemmas.keys():
            pos_freq = find_pos_freq(lemma, dict)
            if len(pos_freq) == 1:
               table.write(lemma + '\t' + str(lemmas[lemma][0]) + '\t' + pos_freq[0][0] + ' \t' + str(pos_freq[0][1]) + '\n')
            else:
                for sentence in lemmas[lemma][1]:
                    for var in pos_freq:
                        if version == '2':
                         # Version 2
                            print(u'Is ' + lemma + u' in the sentence "' + sentence + u'" ' + var[0] + u'? [y/n]')
                            answer = raw_input()
                            if answer == u'y':
                               print 'OK.'
                               if (lemma, var[0], var[1]) not in chosen_pos_freq.keys():
                                   chosen_pos_freq[(lemma, var[0], var[1])] = 1
                               else:
                                   chosen_pos_freq[(lemma, var[0], var[1])] += 1
                               table.write(lemma + '\t' + str(lemmas[lemma][0]) + '\t' + var[0] + '\t' + str(var[1]) + '\n')
                               break
                            else:
                               continue
                        if version == '1':
                        # Version 1
                            table.write(lemma + '\t' + str(lemmas[lemma][0]) + '\t' + var[0] + '\t' + str(var[1]) + '\n')
    if version == '2':
        for lemma in chosen_pos_freq.keys():
            table.write(lemma[0] + '\t' + str(chosen_pos_freq[lemma]) + '\t' + lemma[1] + '\t' + str(lemma[2]) + '\n')
    print 'Table is created.'

dict_name = sys.argv[1]
input_name = sys.argv[2]
output_name = sys.argv[3]
version = sys.argv[4]

words = load_text(input_name)
lemmas = lemmatize(words)
create_table(dict_name, output_name, lemmas, version)