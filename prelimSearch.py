# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 17:29:57 2019

@author: callu
"""

import wikipedia
import pywikibot
import json

site = pywikibot.Site()

s = wikipedia.search("cheese", results=100)

with open('words.json','r') as f:
    datastore=json.load(f)
    

for a in datastore[0]:
    print(datastore[0][a])

search = site.search(searchstring="cheese", where='text', namespaces=[0])

print(s)
i=0
for page in search:
    print(page)
    i +=1
    if i>100:
        break