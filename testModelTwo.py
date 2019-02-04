# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 12:08:21 2018

@author: callu
"""

import json, random, itertools
from gensim.models import Word2Vec, KeyedVectors

with open('words.json','r') as f:
    datastore=json.load(f)
random.seed()
n = 0;
spaces = {}
wordlist = []
for r in range(0,len(datastore[0])-1):
    #print(datastore[0]["WORD"+str(r+1)].lower())
    wordlist.append(datastore[0]["WORD"+str(r+1)].lower().replace(" ", "_"))
    if (datastore[0]["WORD"+str(r+1)].lower().find(" ")) != -1:
        spaces[datastore[0]["WORD"+str(r+1)].lower()] = datastore[0]["WORD"+str(r+1)].lower().replace(" ", "_")

model = Word2Vec.load("w2v2.model")

for word in wordlist:
    print(word)
    print(model.most_similar(word,topn=5))
    print("=====")