# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 20:45:11 2018

@author: callu
"""

import pywikibot, json, os, sys, wikipedia
import nltk, re, time, string
from tqdm import tqdm
import random
from nltk.corpus import stopwords,brown,gutenberg,abc,genesis,subjectivity
from nltk.tokenize import TweetTokenizer
from gensim.models import Word2Vec, KeyedVectors

b = brown.raw()
sense = gutenberg.raw('austen-sense.txt')
emma = gutenberg.raw('austen-emma.txt')
persuasion = gutenberg.raw('austen-persuasion.txt')
bible = genesis.raw('english-kjv.txt')
blake = gutenberg.raw('blake-poems.txt')
bryant = gutenberg.raw('bryant-stories.txt')
burgess= gutenberg.raw('burgess-busterbrown.txt')
carroll = gutenberg.raw('carroll-alice.txt')
ch_ball = gutenberg.raw('chesterton-ball.txt')
ch_brown = gutenberg.raw('chesterton-brown.txt')
ch_thurs = gutenberg.raw('chesterton-thursday.txt')
edge = gutenberg.raw('edgeworth-parents.txt')
mel = gutenberg.raw('melville-moby_dick.txt')
mil = gutenberg.raw('milton-paradise.txt')
caesar = gutenberg.raw('shakespeare-caesar.txt')
hamlet = gutenberg.raw('shakespeare-hamlet.txt')
macbeth = gutenberg.raw('shakespeare-macbeth.txt')
whit = gutenberg.raw('whitman-leaves.txt')
rural = abc.raw('rural.txt')
science = abc.raw('science.txt')
plots = subjectivity.raw('plot.tok.gt9.5000')
quotes = subjectivity.raw('quote.tok.gt9.5000')
austen = sense+emma+persuasion
shakespeare = caesar+hamlet+macbeth
facts = rural+science
opinions = plots+quotes
gute = bryant+burgess+carroll+edge+mel+mil+whit
chester = ch_ball+ch_brown+ch_thurs
total = austen+shakespeare+facts+opinions+gute+chester+b

spaces = {}
wordlist = []

with open('words.json','r') as f:
    datastore=json.load(f)

for r in range(0,len(datastore[0])-1):
    #print(datastore[0]["WORD"+str(r+1)].lower())
    wordlist.append(datastore[0]["WORD"+str(r+1)].lower().replace(" ", "_"))
    if (datastore[0]["WORD"+str(r+1)].lower().find(" ")) != -1:
        spaces[datastore[0]["WORD"+str(r+1)].lower()] = datastore[0]["WORD"+str(r+1)].lower().replace(" ", "_")
        
print(spaces)       

l = 0
total = nltk.tokenize.sent_tokenize(total)
total_sents = []
addstop = ["¬","£"]
nonstop = ['being', 'doing', 'against', 'between', 'during', 'before', 'after', 'above', 'below', 'up', 'down', 'on', 'off', 'over', 'under', 'ma']
stop = stopwords.words('english') + list(string.punctuation) + addstop
stop = list(set([item for item in stop if item not in nonstop]))
first = True
for loop in range(2):
    random.seed(loop)
    random.shuffle(wordlist)
    random.shuffle(total)
    print(type(total))
    print(type(total[0]))
    for word in tqdm(wordlist):
        l += 1
        with open("./corpora/preprocessed/sent_"+word+"_tot.json", "r") as f:
            sents = json.load(f)
        #print(word)
        total_sents += sents
        #for line in sents:
         #   print(line+"\n============")
        if wordlist.index(word) == len(wordlist)-1:
            random.shuffle(total_sents)
            for i, line in enumerate(total_sents):
                total_sents[i] = line.lower()
                #print (total_sents[i])
                for dual in spaces:
                    total_sents[i] = total_sents[i].replace(dual, spaces[dual])
                #print (total_sents[i])
                total_sents[i] = nltk.tokenize.word_tokenize(total_sents[i])
                total_sents[i] = [w for w in total_sents[i] if w not in stop]
                #print (total_sents[i])
            try:
                print("\n\ntrying to train\n\n")
                token_count = sum([len(sent) for sent in total_sents])
                model.build_vocab(sentences=total_sents, update=True)
                print("Vocab updated")
                model.train(total_sents, total_examples = token_count, epochs=10-(loop*3))
            except (NameError, AttributeError):
                print("NAMEATTERROR")
                model = Word2Vec(sentences=total_sents, sg=1, window=10, size=300, min_count=100, max_vocab_size=None, max_final_vocab=800000, workers=12, iter=10)
                model.save("w2vtemp.model")
                model = Word2Vec.load("w2vtemp.model")
            finally:
                total_sents = []
        if (l>50):
            l=0
            random.shuffle(total_sents)
            for i, line in enumerate(total_sents):
                total_sents[i] = line.lower()
                #print (total_sents[i])
                for dual in spaces:
                    total_sents[i] = total_sents[i].replace(dual, spaces[dual])
                #print (total_sents[i])
                total_sents[i] = nltk.tokenize.word_tokenize(total_sents[i])
                total_sents[i] = [w for w in total_sents[i] if w not in stop]
            try:
                print("\n\ntrying to train\n\n")
                token_count = sum([len(sent) for sent in total_sents])
                model.build_vocab(sentences=total_sents, update=True)
                print("Vocab updated")
                model.train(total_sents, total_examples = token_count, epochs=10-(loop*3))
            except (NameError, AttributeError):
                print("NAMEATTERROR")
                model = Word2Vec(sentences=total_sents, sg=1, window=10, size=300, min_count=100, max_vocab_size=None, max_final_vocab=800000, workers=12, iter=10)
                print(type(model))
                model.save("w2vtemp.model")
                model = Word2Vec.load("w2vtemp.model")
                print(type(model))
            finally:
                total_sents = []     
    
    if first == True and (loop%2)==0:
        for i, line in enumerate(total):
            total[i] = line.lower()
            #print (total[i])
            for dual in spaces:
                total[i] = total[i].replace(dual, spaces[dual])
            #print (total[i])
            total[i] = nltk.tokenize.word_tokenize(total[i])
            total[i] = [w for w in total[i] if w not in stop]
            #print (total[i])
        first=False
    
        print("\n\ntrying to train\n\n")
        token_count = sum([len(sent) for sent in total])
    model.build_vocab(sentences=total, update=True)    
    model.train(total, total_examples = token_count, epochs=10-(loop*3))
    
model.save("w2vMega5.model")
model.wv.save_word2vec_format('modelMega5.bin', binary=True)