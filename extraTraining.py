# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 15:19:00 2018

@author: callu
"""
import pywikibot, json, os, sys, wikipedia
import nltk, re, time, string
from tqdm import tqdm
from nltk.corpus import stopwords,brown,gutenberg,abc,genesis,subjectivity
from nltk.tokenize import TweetTokenizer
from gensim.models import Word2Vec, KeyedVectors

spaces = {}
wordlist = []

with open('words.json','r') as f:
    datastore=json.load(f)

for r in range(0,len(datastore[0])-1):
    #print(datastore[0]["WORD"+str(r+1)].lower())
    wordlist.append(datastore[0]["WORD"+str(r+1)].lower().replace(" ", "_"))
    if (datastore[0]["WORD"+str(r+1)].lower().find(" ")) != -1:
        spaces[datastore[0]["WORD"+str(r+1)].lower()] = datastore[0]["WORD"+str(r+1)].lower().replace(" ", "_")
        
model = Word2Vec.load("w2v.model")
model2 = Word2Vec.load("w2v2.model")

b = brown.raw()
print(b[0])
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

print(total[0])
print(total[1])
print(total[2])
print(total[3])
print(total[4])

total = nltk.tokenize.sent_tokenize(total)

print(total[0])
print(total[1])
print(total[2])
print(total[3])
print(total[4])

#sys.exit()

stop = stopwords.words('english') + list(string.punctuation)

for i, line in enumerate(total):
    total[i] = line.lower()
    #print (total[i])
    for dual in spaces:
        total[i] = total[i].replace(dual, spaces[dual])
    #print (total[i])
    total[i] = nltk.tokenize.word_tokenize(total[i])
    total[i] = [w for w in total[i] if w not in stop]
    #print (total[i])

print("\n\ntrying to train\n\n")
token_count = sum([len(sent) for sent in total])
    
model.train(total, total_examples = token_count, epochs=5)
model2.train(total, total_examples = token_count, epochs=5)
    
model.save("w2v3.model")
model.wv.save_word2vec_format('model4.bin', binary=True)
model2.save("w2v4.model")
model2.wv.save_word2vec_format('model5.bin', binary=True)