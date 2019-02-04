# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 15:23:13 2018

@author: Callum Marvell
"""

import json, random, itertools, re
from gensim.models import Word2Vec, KeyedVectors
from nltk.stem import WordNetLemmatizer
import numpy as np
import scipy as sp
import os, wikipedia, sys
from nltk.corpus import wordnet as wn
from nltk.tokenize import TweetTokenizer

wordnet_lemmatizer = WordNetLemmatizer()
tknzr = TweetTokenizer()

def fixCompound(word):
    bork = ["ice_cream", "new_york", "loch_ness", "scuba_diver"]
    fix = ["ice cream", "new york", "loch ness", "scuba diver"]
    try:
        res = bork.index(word)
        return(fix[res])
    except:
        return word

with open('words.json','r') as f:
    datastore=json.load(f)

all = []    
for key in datastore[0]:
    all.append(datastore[0][key])
    
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

def lchSim(word1, word2, thresh, verbose):
    results = []
    lch_threshold = thresh
    if not word1==word2:
        for net1 in wn.synsets(word1):
            for net2 in wn.synsets(word2):
                try:
                    lch = net1.lch_similarity(net2)
                    if lch >= lch_threshold:
                        results.append((net1, net2))
                except:
                    continue
    if not results:
            return False
    if verbose:
        for net1, net2 in results:
            print (net1)
            print (net1.definition)
            print (net2)
            print (net2.definition)
            print ('path similarity:')
            print (net1.path_similarity(net2))
            print ('lch similarity:')
            print (net1.lch_similarity(net2))
            print ('wup similarity:')
            print (net1.wup_similarity(net2))
            print ('-' * 79)
    return True

two = list(itertools.combinations(redwords,2))
good = []

threshold = 2.15

while not good:
    print(threshold)
    for pair in two:
        word1 = pair[0]
        word2 = pair[1]
        if lchSim(word1, word2, threshold, False):
            print(word1+" "+word2)
            #lchSim(word1, word2, 2.2, True)
            good.append(pair)
    threshold -= 0.05

print("titles")
for pair in good:
    done = False
    w1 = fixCompound(pair[0])
    w2 = fixCompound(pair[1])
    with open('corpora/searches/'+w1+'.json','r') as f:
        res1=json.load(f)
    with open('corpora/searches/'+w2+'.json','r') as f:
        res2=json.load(f)
    for result in res1:
        if result in res2:
            print(w1+" "+w2+" "+result)
            done = True
    if not done:
        res1 = wikipedia.search(w1, results=3000)
        res2 = wikipedia.search(w2, results=3000)
        for result in res1:
            if result in res2:
                print("NOT DONE: "+w1+" "+w2+" "+result)
        with open('corpora/searches/'+w1+'.json','r') as f:
            res1=json.load(f)
        with open('corpora/searches/'+w2+'.json','r') as f:
            res2=json.load(f)
        for result in res1:
            split = tknzr.tokenize(result)
            for word in split:
                word = word.replace("(", "")
                word = word.replace(")", "")
                test = re.compile("\b"+word+"\b")
                for result2 in res2:
                    if re.search(test,result2):
                        print("NOT DONE - REGEX: "+w1+" "+w2+" "+result2)
                        break

print("=========")

good = [("ice_cream", "cold")]
for pair in good:
    done = False
    w1 = fixCompound(pair[0])
    w2 = fixCompound(pair[1])
    with open('corpora/searches/'+w1+'.json','r') as f:
        res1=json.load(f)
    with open('corpora/searches/'+w2+'.json','r') as f:
        res2=json.load(f)
    for result in res1:
        if result in res2:
            print(w1+" "+w2+" "+result)
            done = True
    if not done:
        res1 = wikipedia.search(w1, results=3000)
        res2 = wikipedia.search(w2, results=3000)
        for result in res1:
            if result in res2:
                print("NOT DONE: "+w1+" "+w2+" "+result)
        with open('corpora/searches/'+w1+'.json','r') as f:
            res1=json.load(f)
        with open('corpora/searches/'+w2+'.json','r') as f:
            res2=json.load(f)
        for result in res1:
            split = tknzr.tokenize(result)
            for word in split:
                word = word.replace("(", "")
                word = word.replace(")", "")
                test = re.compile("\b"+word+"\b")
                for result2 in res2:
                    if re.search(test,result2):
                        print("NOT DONE - REGEX: "+w1+" "+w2+" "+result2)
                        break
    
sys.exit()
three = list(itertools.combinations(redwords,3))
four = list(itertools.combinations(redwords,4))
five = list(itertools.combinations(redwords,5))

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

good = redwords
bad = bluewords
good_ind = [model.vocab[stem(fixWord(word))].index for word in good]
#print(good_ind)
good_vec = model.vectors_norm[good_ind]
bad_ind = [model.vocab[stem(fixWord(word))].index for word in bad]
bad_vec = model.vectors_norm[bad_ind]
by_ind = [model.vocab[stem(fixWord(word))].index for word in bywords]
by_vec = model.vectors_norm[by_ind]
ass_ind = model.vocab[stem(fixWord(assassin))].index
ass_vec = model.vectors_norm[ass_ind]

good_mean = np.mean(good_vec, axis=0)
bad_mean = np.mean(bad_vec, axis=0)
by_mean = np.mean(by_vec, axis=0)

def mostSim(clueset, goodset, badset, byset, ass):
    best = 5
    bestC = ()
    bestR = float("inf")
    for words in clueset:
        clue_ind = [model.vocab[stem(fixWord(word))].index for word in words]
        clue_vec = model.vectors_norm[clue_ind]
        clue_mean = np.mean(clue_vec, axis=0)
        total_dist = 0.0
        count = 0
        for word in words:
            test_vec = model.vectors_norm[model.vocab[stem(fixWord(word))].index]
            dist = sp.spatial.distance.cosine(test_vec, clue_mean)
            total_dist += dist
            count += 1
        if total_dist < best:
            risk = 0
            for word in words:
                risk_vec = model.vectors_norm[model.vocab[stem(fixWord(word))].index]
                for good in goodset:
                    good = fixWord(good)
                    good_ind = model.vocab[stem(good)].index
                    good_vec = model.vectors_norm[good_ind]
                    dist = sp.spatial.distance.cosine(risk_vec, good_vec)
                    risk -= 1*dist
                    good_ind = model.vocab[good].index
                    good_vec = model.vectors_norm[good_ind]
                    dist = sp.spatial.distance.cosine(risk_vec, good_vec)
                    risk -= 1*dist
                for bad in badset:
                    bad = fixWord(bad)
                    bad_ind = model.vocab[stem(bad)].index
                    bad_vec = model.vectors_norm[bad_ind]
                    dist = sp.spatial.distance.cosine(risk_vec, bad_vec)
                    risk += 3*dist
                    bad_ind = model.vocab[bad].index
                    bad_vec = model.vectors_norm[bad_ind]
                    dist = sp.spatial.distance.cosine(risk_vec, bad_vec)
                    risk += 3*dist
                for by in byset:
                    by = fixWord(by)
                    by_ind = model.vocab[stem(by)].index
                    by_vec = model.vectors_norm[by_ind]
                    dist = sp.spatial.distance.cosine(risk_vec, by_vec)
                    risk += dist*2
                    by_ind = model.vocab[by].index
                    by_vec = model.vectors_norm[by_ind]
                    dist = sp.spatial.distance.cosine(risk_vec, by_vec)
                    risk += dist*2
                ass = fixWord(ass)
                ass_ind = model.vocab[stem(ass)].index
                ass_vec = model.vectors_norm[ass_ind]
                dist = sp.spatial.distance.cosine(risk_vec, ass_vec)
                risk += dist*50
                ass_ind = model.vocab[ass].index
                ass_vec = model.vectors_norm[ass_ind]
                dist = sp.spatial.distance.cosine(risk_vec, ass_vec)
                risk += dist*50
                #print("RISK: "+str(risk))
            if risk < bestR:
                print("RISK: "+str(risk))
                bestC = words
                best = total_dist
                bestR = risk
    return bestC

def illegalClues(words):
    result = []
    best = 1
    for part in words:
        part_vec = model.vectors_norm[model.vocab[stem(fixWord(part))].index]
        for word in model.vocab:
            test_vec = model.vectors_norm[model.vocab[stem(fixWord(word))].index]
            part_dist = sp.spatial.distance.cosine(test_vec, part_vec)
            if part_dist < best:
                best = part_dist
            if part_dist < 0.01:
                result.append(word)
    #print(best)
    return result

def getRisk(word, goodset, badset, byset, ass):
    risk = 0
    risk_vec = model.vectors_norm[model.vocab[stem(fixWord(word))].index]
    for good in goodset:
        good = fixWord(good)
        good_ind = model.vocab[stem(good)].index
        good_vec = model.vectors_norm[good_ind]
        dist = sp.spatial.distance.cosine(risk_vec, good_vec)
        risk -= 1*dist
        good_ind = model.vocab[good].index
        good_vec = model.vectors_norm[good_ind]
        dist = sp.spatial.distance.cosine(risk_vec, good_vec)
        risk -= 1*dist
    for bad in badset:
        bad = fixWord(bad)
        bad_ind = model.vocab[stem(bad)].index
        bad_vec = model.vectors_norm[bad_ind]
        dist = sp.spatial.distance.cosine(risk_vec, bad_vec)
        risk += 3*dist
        bad_ind = model.vocab[bad].index
        bad_vec = model.vectors_norm[bad_ind]
        dist = sp.spatial.distance.cosine(risk_vec, bad_vec)
        risk += 3*dist
    for by in byset:
        by = fixWord(by)
        by_ind = model.vocab[stem(by)].index
        by_vec = model.vectors_norm[by_ind]
        dist = sp.spatial.distance.cosine(risk_vec, by_vec)
        risk += dist*2
        by_ind = model.vocab[by].index
        by_vec = model.vectors_norm[by_ind]
        dist = sp.spatial.distance.cosine(risk_vec, by_vec)
        risk += dist*2
    ass = fixWord(ass)
    ass_ind = model.vocab[stem(ass)].index
    ass_vec = model.vectors_norm[ass_ind]
    dist = sp.spatial.distance.cosine(risk_vec, ass_vec)
    risk += dist*50
    ass_ind = model.vocab[ass].index
    ass_vec = model.vectors_norm[ass_ind]
    dist = sp.spatial.distance.cosine(risk_vec, ass_vec)
    risk += dist*50
    return risk

def clueValue(cluewords, goodset, badset, byset, ass):
    illegal = illegalClues(cluewords)
    raw_promise = np.full(10, 100000, dtype=float)
    init_promise = np.ones(10, dtype=float)
    str_promise = np.empty(10, dtype=object)
    clue_ind = [model.vocab[stem(fixWord(word))].index for word in cluewords]
    clue_vec = model.vectors_norm[clue_ind]
    clue_mean = np.mean(clue_vec, axis=0)
    for word in model.vocab:
        valid = True
        for ex in illegal:
            if ex == word:
                valid = False
        if valid == True:
            test_vec = model.vectors_norm[model.vocab[word].index]
            clue_dist = sp.spatial.distance.cosine(test_vec, clue_mean)
            if(clue_dist<init_promise[0]):
                risk = getRisk(word, goodset, badset, byset, ass)
                if((clue_dist*risk)<raw_promise[0]):
                    init_promise[0] = clue_dist
                    init_promise = sorted(init_promise, reverse=True)
                    raw_promise[0] = clue_dist*risk
                    str_promise[0] = word
                    raw_promise, str_promise = (list(t) for t in zip(*sorted(zip(raw_promise, str_promise), reverse=True)))
    print(raw_promise)
    res = [x*len(cluewords) for x in raw_promise]
    return res, str_promise

print(clueValue(["bugle", "roulette", "washer", "ice cream", "new york", "loch ness", "scuba diver"], redwords, bluewords, bywords, assassin))

print(redwords)
res = mostSim(two, redwords, bluewords, bywords, assassin)

dos = mostSim(two, redwords, bluewords, bywords, assassin)
tres = mostSim(three, redwords, bluewords, bywords, assassin)
cuatro = mostSim(four, redwords, bluewords, bywords, assassin)
cinco = mostSim(five, redwords, bluewords, bywords, assassin)
print("============")
print(dos)
print(clueValue(dos, redwords, bluewords, bywords, assassin))
print("============")
print(tres)
print(clueValue(tres, redwords, bluewords, bywords, assassin))
print("============")
print(cuatro)
print(clueValue(cuatro, redwords, bluewords, bywords, assassin))
print("============")
print(cinco)
print(clueValue(cinco, redwords, bluewords, bywords, assassin))
    