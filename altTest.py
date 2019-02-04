# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 14:41:44 2018

@author: callu
"""

import json, random, itertools
from gensim.models import Word2Vec, KeyedVectors

with open('words.json','r') as f:
    datastore=json.load(f)
random.seed()
n = 0;
wordset = []
while len(wordset)<25:
    r = random.randint(0,len(datastore[0])-1)
    if datastore[0]["WORD"+str(r+1)].lower() not in wordset:
        print("|"+datastore[0]["WORD"+str(r+1)].lower()+"|", end="")
        wordset.append(datastore[0]["WORD"+str(r+1)].lower())
    else:
        continue
    n+=1
    if n>=5:
        print("\n")
        n=0

model = Word2Vec.load("w2vTitle.model")

for i in range(10):
    r1 = random.randint(0,24)
    r2 = random.randint(0,24)
    print(wordset[r1]+" "+wordset[r2])
    print(model.most_similar(positive=[wordset[r1],wordset[r2]], topn=5))

