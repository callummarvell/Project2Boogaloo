# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 12:56:54 2018

@author: callu
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 15:23:13 2018

@author: Callum Marvell
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

model = Word2Vec.load("w2v2.model")
model2 = Word2Vec.load("w2v4.model")

#for word in redwords:
#    print(model.most_similar(positive=word))
two = list(itertools.combinations(redwords,2))
three = list(itertools.combinations(redwords,3))
four = list(itertools.combinations(redwords,4))
five = list(itertools.combinations(redwords,5))


"""
for pair in two:
    try:
        print (pair)
        print (model.similarity(pair[0],pair[1]))
        print (model.most_similar(positive=[pair[0],pair[1]], topn=5))
    #for sim in model.most_similar(pair[0],topn=50):
    #    #print (sim[0]+"\n")
    #    sim_list = [x[0] for x in model.most_similar(pair[1],topn=50)]
    #    if sim[0] in sim_list:
    #        print (sim)
    except KeyError:
        continue

twoa = list(itertools.combinations(bluewords,2))

for pair in twoa:
    try:
        print (pair)
        print (model.similarity(pair[0],pair[1]))
        print (model.most_similar(positive=[pair[0],pair[1]], topn=5))
    #for sim in model.most_similar(pair[0],topn=50):
    #    #print (sim[0]+"\n")
    #    sim_list = [x[0] for x in model.most_similar(pair[1],topn=50)]
    #    if sim[0] in sim_list:
    #        print (sim)
    except KeyError:
        continue
"""    
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
        #for sim in model.most_similar(pair[0],topn=50):
        #    #print (sim[0]+"\n")
        #    sim_list = [x[0] for x in model.most_similar(pair[1],topn=50)]
        #    if sim[0] in sim_list:
        #        print (sim)
        except KeyError:
            continue
    print (w1, w2, float(best))
    print (w1, w2, model.most_similar(positive=[w1,w2], topn=8))
    print (w3, w4, model.similarity(w3,w4))
    print (w3, w4, model.most_similar(positive=[w3,w4], topn=8))

getSims(two,model)
print("===========")
getSims(two,model2)
print("++++++++")
print(model.most_similar(positive=["cheese","bread"]))
print(model2.most_similar(positive=["cheese","bread"]))
print(model.most_similar(positive=["cheese","bread"], negative=["sandwich"]))
print(model2.most_similar(positive=["cheese","bread"], negative=["sandwich"]))
#getSims(three)
#print("===========")
#getSims(four)
#print("===========")
#getSims(five)