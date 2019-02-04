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

model = KeyedVectors.load_word2vec_format("modelMega.bin", binary=True)
#model2 = Word2Vec.load("w2vTitle.model")
model.init_sims(replace=True)

#for word in redwords:
#    print(model.most_similar(positive=word))
two = list(itertools.combinations(redwords,2))
three = list(itertools.combinations(redwords,3))
four = list(itertools.combinations(redwords,4))
five = list(itertools.combinations(redwords,5))

def getSims(words, model):
    num = len(words[0])
    w1 = ""
    w2 = ""
    w3 = ""
    w4 = ""
    best = float(0.0)
    best2 = float(0.0)
    for comb in words:
        pos = []
        for i in range(num):
            pos.append(comb[i])
        try:
            print (comb)
            print (model.similarity(comb[0],comb[1]))
            if (model.similarity(comb[0],comb[1])>best):
                w1 = comb[0]
                w2 = comb[1]
                best = model.similarity(comb[0],comb[1])
            #print (model.most_similar(positive=pos, topn=8))
            for word in model.most_similar(positive=pos, topn=8):
                if word[1]>best2:
                    best2 = word[1]
                    w3 = comb[0]
                    w4 = comb[1]
        except KeyError:
            continue
    print (w1, w2, float(best))
    print (w1, w2, model.most_similar(positive=[w1,w2], topn=8))
    print (w3, w4, model.similarity(w3,w4))
    print (w3, w4, model.most_similar(positive=[w3,w4], topn=8))

"""
getSims(two,model)
print("===========")
getSims(two,model2)
print("++++++++")
print(model.most_similar(positive=["cheese"]))
print(model2.most_similar(positive=["cheese"]))"""

#for word in model.wv.vocab:
#    print(word)
    
#for vec in model.wv.syn0norm:
#    print(vec)

#redwords=["house","city"]

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
    best = 2
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
            #print(best)
    return bestC

def searchCheck(term, word):
    #word = fixWord(word)
    word = word.replace("_", " ")
    test = re.compile('\b'+term+'\b')
    with open('corpora/searches/'+str(word.capitalize())+'.json','r') as f:
        current = json.load(f)
    for result in current:
        if re.search(test,result):
            return True
    return False

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
                for clue in cluewords:
                    if searchCheck(word,clue):
                        risk = risk*0.8
                if((clue_dist*risk)<raw_promise[0]):
                    init_promise[0] = clue_dist
                    init_promise = sorted(init_promise, reverse=True)
                    raw_promise[0] = clue_dist*risk
                    str_promise[0] = word
                    raw_promise, str_promise = (list(t) for t in zip(*sorted(zip(raw_promise, str_promise), reverse=True)))
    print(raw_promise)
    res = [x*len(cluewords) for x in raw_promise]
    return res, str_promise

#print(good_vec[:2])
#print(np.mean(good_vec, axis=0))

"""
for word in model.vocab:
    test_vec = model.vectors_norm[model.vocab[word].index]
    good_dist = sp.spatial.distance.cosine(test_vec, good_mean)
    if(good_dist<raw_promise[0]):
        raw_promise[0] = good_dist
        str_promise[0] = word
        raw_promise, str_promise = (list(t) for t in zip(*sorted(zip(raw_promise, str_promise), reverse=True)))
"""

#print(redwords)
#print(str_promise)
print(clueValue(["bugle", "roulette", "washer", "ice cream", "new york", "loch ness", "scuba diver"], redwords, bluewords, bywords, assassin))

print(redwords)
#res = mostSim(two, redwords, bluewords, bywords, assassin)

dos = mostSim(two, redwords, bluewords, bywords, assassin)
tres = mostSim(three, redwords, bluewords, bywords, assassin)
cuatro = mostSim(four, redwords, bluewords, bywords, assassin)
cinco = mostSim(five, redwords, bluewords, bywords, assassin)
print("============")
print(dos)
#print(illegalClues(("angel","spell")))
#print(illegalClues(res))
print(clueValue(dos, redwords, bluewords, bywords, assassin))
#print(clueValue(("maple","tree")))
print("============")
print(tres)
print(clueValue(tres, redwords, bluewords, bywords, assassin))
print("============")
print(cuatro)
print(clueValue(cuatro, redwords, bluewords, bywords, assassin))
print("============")
print(cinco)
print(clueValue(cinco, redwords, bluewords, bywords, assassin))

#for comb in two:
#    print(comb)
#    print(clueValue(comb))
    
    