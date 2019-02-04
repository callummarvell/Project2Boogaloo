# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 18:07:53 2018

@author: callu
"""

from gensim.models import Word2Vec, KeyedVectors
import json, time, sys

wordlist = []

with open('words.json','r') as f:
    datastore=json.load(f)

for r in range(0,len(datastore[0])-1):
    #print(datastore[0]["WORD"+str(r+1)].lower())
    wordlist.append(datastore[0]["WORD"+str(r+1)].lower().replace(" ", "_"))
    
model = Word2Vec.load("w2v.model")
#for word in model.wv.vocab:
#    print("\n========\n"+word+"\n=========\n")
#    time.sleep(2)
#word_vectors = model.wv
#word_vectors.save("word_Vectors.bin")
#word_vectors = KeyedVectors.load("word_Vectors.bin", mmap='r')
#g = KeyedVectors.load_word2vec_format('./model2.bin', binary=True)

"""
for word in wordlist:
    try:
        print(word)
        print(model.most_similar(word, topn=10))
        print("\n")
    except KeyError:
        print(word+" not in vocab\n")
        continue
"""

