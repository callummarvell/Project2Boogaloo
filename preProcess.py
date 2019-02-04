# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 20:49:55 2018

@author: callu
"""

import pywikibot, json, os, sys, wikipedia
import nltk, re

wordlist = []
spaces = {}

with open('words.json','r') as f:
    datastore=json.load(f)

for r in range(0,len(datastore[0])-1):
    #print(datastore[0]["WORD"+str(r+1)].lower())
    wordlist.append(datastore[0]["WORD"+str(r+1)].lower())
    if (datastore[0]["WORD"+str(r+1)].lower().find(" ")) != -1:
        spaces[datastore[0]["WORD"+str(r+1)].lower()] = datastore[0]["WORD"+str(r+1)].lower().replace(" ", "_")

try:
    os.mkdir("corpora")
    os.chdir("corpora")
except OSError:
    os.chdir("corpora")

headings = re.compile('=+ ([^=]+) =+\s*')

files = os.listdir()
try:
    os.mkdir("preprocessed")
    os.chdir("preprocessed")
except OSError:
    os.chdir("preprocessed")
    

"""
for name in files:
    if not os.path.isfile(name):
        print(name)
        if name.find("_tot.json") != -1:
            with open("../"+name,'r') as f:
                content = json.load(f)
            f.close()
            with open(name,'w') as f:
                content = re.sub(headings, '', content)
                json.dump(content, f)
                with open("sent_"+name,'w') as f2:
                    content2 = nltk.tokenize.sent_tokenize(content)
                    for line in content2:
                        for word in spaces:
                            line = line.replace(word, spaces[word])
                    json.dump(content2, f2)
                f2.close()
            f.close()
"""
      
results = os.listdir()
complete = ""
content = ""
for name in results:
    if name.find("sent_") == -1:
        with open(name,'r') as f:
            content = json.load(f)
        f.close()
        complete += content

print (type(complete))

with open("complete.txt",'w') as f:
    f.write(complete)
f.close()


#for sent in complete[0:12]:
#    print(sent+"\n")

#print(content)

#print("\n\n"+sentTokenizer.tokenize(page)[2])

