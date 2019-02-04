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

all = []
for r in range(0,len(datastore[0])-1):
    #print(datastore[0]["WORD"+str(r+1)].lower())
    all.append(datastore[0]["WORD"+str(r+1)])
    wordlist.append(datastore[0]["WORD"+str(r+1)].lower().replace(" ", "_"))
    if (datastore[0]["WORD"+str(r+1)].lower().find(" ")) != -1:
        spaces[datastore[0]["WORD"+str(r+1)].lower()] = datastore[0]["WORD"+str(r+1)].lower().replace(" ", "_")
       
model = Word2Vec.load("w2vMega.model")

total = []
totalstr = ""

for word in wordlist:
    with open('corpora/'+str(word)+'.json','r') as f:
        current = json.load(f)
        total.append(current)
for word in all:
    with open('corpora/searches/'+str(word)+'.json','r') as f:
        current = json.load(f)
        total.append(current)

#print(total[0])
#print(total[1])
#print(total[2])
#print(total[3])
#print(total[4])

totalstr = ""
for i, ent in enumerate(total):
    entstr = ""
    for title in total[i]:
        entstr += title
        entstr += " "
    totalstr += entstr

total = nltk.tokenize.sent_tokenize(totalstr)

#print(total[0])
#print(total[1])
#print(total[2])
#print(total[3])
#print(total[4])

#sys.exit()

stop = stopwords.words('english') + list(string.punctuation)

for i, line in enumerate(tqdm(total)):
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
    
model.save("w2vTitleI.model")
model.wv.save_word2vec_format('modelTI.bin', binary=True)