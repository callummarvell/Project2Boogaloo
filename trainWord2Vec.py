# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 20:45:11 2018

@author: callu
"""

import pywikibot, json, os, sys, wikipedia
import nltk, re, time, string
from tqdm import tqdm
from nltk.corpus import stopwords
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
        
print(spaces)       

l = 0
total_sents = []
stop = stopwords.words('english') + list(string.punctuation)

for word in tqdm(wordlist):
    l += 1
    with open("./corpora/preprocessed/sent_"+word+"_tot.json", "r") as f:
        sents = json.load(f)
    #print(word)
    total_sents += sents
    #for line in sents:
     #   print(line+"\n============")
    if wordlist.index(word) == len(wordlist)-1:
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
            model.train(total_sents, total_examples = token_count, epochs=self.iter)
        except NameError:
            model = Word2Vec(sentences=total_sents, size=300, min_count=1, max_vocab_size=None, max_final_vocab=None, workers=12, iter=5)
        finally:
            total_sents = []
    if (l>50):
        l=0
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
            model.train(total_sents, total_examples = token_count, epochs=self.iter)
        except NameError:
            model = Word2Vec(sentences=total_sents, size=300, min_count=1, max_vocab_size=None, max_final_vocab=None, workers=12, iter=5)
        finally:
            total_sents = []
model.save("w2v.model")
model.wv.save_word2vec_format('model2.bin', binary=True)