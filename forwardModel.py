# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 16:55:55 2019

@author: callu
"""

import json, random, itertools, re, math
from gensim.models import Word2Vec, KeyedVectors
from nltk.stem import WordNetLemmatizer
import numpy as np
import scipy as sp
from gameLoopAIMaster import turn, win, checkGuess
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

def findClue(goodwords, badwords, bywords, assassin):    
    def mostSim(clueset, goodset, badset, byset, ass):
        best = float("inf")
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
        return bestC, bestR
    
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
                #if word.find(".") != -1:
                 #   result.append(word)
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
    
    def clueValue(cluewords, goodset, badset, byset, ass, riskIn):
        illegal = illegalClues(cluewords)
        raw_promise = np.full(1, 100000, dtype=float)
        init_promise = np.ones(1, dtype=float)
        str_promise = np.empty(1, dtype=object)
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
                    risk = getRisk(word, goodset, badset, byset, ass) * riskIn
                    for clue in cluewords:
                        if searchCheck(word,clue):
                            risk = risk*0.9
                            break
                    if((clue_dist*risk)<raw_promise[0]):
                        init_promise[0] = clue_dist
                        init_promise = sorted(init_promise, reverse=True)
                        raw_promise[0] = clue_dist*risk
                        str_promise[0] = word
                        raw_promise, str_promise = (list(t) for t in zip(*sorted(zip(raw_promise, str_promise), reverse=True)))
        print(raw_promise)
        res = [x/math.sqrt(len(cluewords)) for x in raw_promise]
        print(res)
        return res, str_promise
    
    two = list(itertools.combinations(goodwords,2))
    three = list(itertools.combinations(goodwords,3))
    four = list(itertools.combinations(goodwords,4))
    five = list(itertools.combinations(goodwords,5))
    dos, dosR = mostSim(two, goodwords, badwords, bywords, assassin)
    tres, tresR = mostSim(three, goodwords, badwords, bywords, assassin)
    cuatro, cuatroR = mostSim(four, goodwords, badwords, bywords, assassin)
    cinco, cincoR = mostSim(five, goodwords, badwords, bywords, assassin)
    optimal = float("inf")
    optimalwrd = ""
    length = 1
    print("============")
    print(dos)
    #print(clueValue(dos, goodwords, badwords, bywords, assassin))
    ra,sa = clueValue(dos, goodwords, badwords, bywords, assassin, dosR)
    r = ra[0]
    s = sa[0]
    print(s)
    if (optimal>r):
        optimal = r
        optimalwrd = s
        length = 2
    print("============")
    print(tres)
    #print(clueValue(tres, goodwords, badwords, bywords, assassin))
    ra,sa = clueValue(tres, goodwords, badwords, bywords, assassin, tresR)
    r = ra[0]
    s = sa[0]
    print(s)
    if (optimal>r):
        optimal = r
        optimalwrd = s
        length = 3
    print("============")
    print(cuatro)
    #print(clueValue(cuatro, goodwords, badwords, bywords, assassin))
    ra,sa = clueValue(cuatro, goodwords, badwords, bywords, assassin, cuatroR)
    r = ra[0]
    s = sa[0]
    print(s)
    if (optimal>r):
        optimal = r
        optimalwrd = s
        length = 4
    print("============")
    print(cinco)
    #print(clueValue(cinco, goodwords, badwords, bywords, assassin))
    ra,sa = clueValue(cinco, goodwords, badwords, bywords, assassin, cincoR)
    r = ra[0]
    s = sa[0]
    print(s)
    if (optimal>r):
        optimal = r
        optimalwrd = s
        length = 5
    print("GIVING CLUE: "+optimalwrd+" OF LENGTH: "+str(length))
    return length

#print(findWords(["cat","dog","cow","moose","pan","oven","paint"], "pet", 2))
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
    if current == 0:
        loop = findClue(redwords, bluewords, bywords, assassin)
        for i in range(0,loop+1):
            guess = input("RED TEAM, enter a guess for the clue ")
            dead, wrong = checkGuess(current, guess, redwords, bluewords, bywords, assassin)
            if dead == True or wrong == True: break
        print("RED TEAM, your turn is over")
    else:
        loop = findClue(bluewords, redwords, bywords, assassin)
        for i in range(0,loop+1):
            guess = input("BLUE TEAM, enter a guess for the clue ")
            dead,wrong = checkGuess(current, guess, redwords, bluewords, bywords, assassin)
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