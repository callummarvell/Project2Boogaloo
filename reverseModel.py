# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 16:55:55 2019

@author: callu
"""

import json, random, itertools, re
from gensim.models import Word2Vec, KeyedVectors
from nltk.stem import WordNetLemmatizer
import numpy as np
import scipy as sp
from gameLoopAIPlayer import turn, win, checkGuess
from nltk.corpus import wordnet as wn

wordnet_lemmatizer = WordNetLemmatizer()

with open('words.json','r') as f:
    datastore=json.load(f)
random.seed()
n = 0;
wordset = []
upperset = []
while len(wordset)<25:
    r = random.randint(0,len(datastore[0])-1)
    if datastore[0]["WORD"+str(r+1)].lower() not in wordset:
        print("|"+datastore[0]["WORD"+str(r+1)].lower()+"|", end="")
        wordset.append(datastore[0]["WORD"+str(r+1)].lower())
        upperset.append(datastore[0]["WORD"+str(r+1)])
    else:
        continue
    n+=1
    if n>=5:
        print("\n")
        n=0

#syn_func(datastore[0]["WORD"+str(r+1)])

r2 = random.randint(0,1)

redwords = []
bluewords = []
bywords = []
wordset_copy = wordset

if (r2>0):
    redfirst = 1
    extra = wordset[random.randint(0,24)]
    redwords.append(extra)
    wordset_copy.remove(extra)
else:
    redfirst = 0
    extra = wordset[random.randint(0,24)]
    bluewords.append(extra)
    wordset_copy.remove(extra)
    
for i in range(0,8):
    red = wordset_copy[random.randint(0,len(wordset_copy)-1)]
    redwords.append(red)
    wordset_copy.remove(red)
    blue = wordset_copy[random.randint(0,len(wordset_copy)-1)]
    bluewords.append(blue)
    wordset_copy.remove(blue)

for i in range(0,7):
    bystander = wordset_copy[random.randint(0,len(wordset_copy)-1)]
    bywords.append(bystander)
    wordset_copy.remove(bystander)

assassin=wordset_copy[0]

model = KeyedVectors.load_word2vec_format("modelMega5.bin", binary=True)
model.init_sims(replace=True)

def stem(word):
    try:
        model.vocab[wordnet_lemmatizer.lemmatize(word)].index
        return wordnet_lemmatizer.lemmatize(word)
    except:
        #print(word+" DOESN'T WORK")
        return word
    
def fixWord(word):
    alt = ["trumpet", "gambling", "wash", "ice_cream", "new_york", "loch_ness", "scuba"]
    bork = ["bugle", "roulette", "washer", "ice cream", "new york", "loch ness", "scuba diver"]
    try:
        res = bork.index(word)
        return(alt[res])
    except:
        return word

def findWords(targetset,wholeset,clue,size):
    best_dist = float("inf")
    best = None
    combinations = list(itertools.combinations(wholeset,size))
    #print(combinations)
    clue_vec = model.vectors_norm[model.vocab[fixWord(clue)].index]
    #print(stem(fixWord(clue)))
    def inner(elem):
        test_vec = model.vectors_norm[model.vocab[stem(fixWord(elem))].index]
        dist = sp.spatial.distance.cosine(test_vec, clue_vec)
        return dist
    for combo in combinations:
        total_dist = 0
        for word in combo:
            print(word)
            test_vec = model.vectors_norm[model.vocab[stem(fixWord(word))].index]
            dist = sp.spatial.distance.cosine(test_vec, clue_vec)
            print(dist)
            total_dist += dist
        if (total_dist/size)<best_dist:
            best = sorted(combo, key=inner)
            best_dist = total_dist/size
        print(combo)
        print(total_dist)
    print(best)
    return best,best_dist

#print(findWords([],["cat","dog","cow","moose","pan","oven","paint"], "pet", 2))
#print(findWords([],["capital","lead","van", "church","rome"], "car", 2))
dead=False
current = 1 - redfirst
while (len(redwords)>0 and len(bluewords)>0 and dead!=True):
    print("RED")
    print(redwords)
    print("BLUE")
    print(bluewords)
    remaining = redwords+bluewords+bywords+[assassin]
    random.shuffle(remaining)
    print("REMAINING WORDS\n")
    print(remaining)
    res = turn(current)
    loop = res[0]
    if current == 0:
        default = findWords(redwords,remaining,res[1],res[0])
        extra = findWords(redwords,remaining,res[1],res[0]+1)
        if extra[1]<=default[1]: 
            default = extra
            loop += 1
        for i in range(0,loop):
            print(default[0][i])
            dead, wrong = checkGuess(current, default[0][i], redwords, bluewords, bywords, assassin)
            if dead == True or wrong == True: break
        print("RED TEAM, your turn is over")
    else:
        default = findWords(bluewords,remaining,res[1],res[0])
        extra = findWords(bluewords,remaining,res[1],res[0]+1)
        if extra[1]<=default[1]: 
            default = extra
            loop += 1
        for i in range(0,loop):
            print(default[0][i])
            dead,wrong = checkGuess(current, default[0][i], redwords, bluewords, bywords, assassin)
            if dead == True or wrong == True: break
        print("BLUE TEAM, your turn is over")
    current=1-current
if (dead==True):
    win(current)
elif (len(bluewords)==0):
    win(1)
else:
    win(0)
#STILL NEED  TO MAKE THE WHOLE THING LOOP