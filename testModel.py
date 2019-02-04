# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 11:40:12 2018

@author: Callum Marvell
"""
from gensim.models import Word2Vec, KeyedVectors
import json, gensim

wordlist = []

with open('words.json','r') as f:
    datastore=json.load(f)

for r in range(0,len(datastore[0])-1):
    #print(datastore[0]["WORD"+str(r+1)].lower())
    wordlist.append(datastore[0]["WORD"+str(r+1)].lower().replace(" ", "_"))
    
model = KeyedVectors.load_word2vec_format("model.bin", binary=True)

for word in wordlist:
    try:
        print(word)
        print(model.most_similar(word, topn=10))
        print("\n")
    except KeyError:
        print (word+" not in vocab")
        continue