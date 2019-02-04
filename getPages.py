# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 20:21:24 2018

@author: callu
"""

import pywikibot, json, nltk, os, sys

site = pywikibot.Site()

print(pywikibot.Page(site, u"cheese").text)
sys.exit()

def pull(page, page_titles, max_pages, depth, max_depth):
    try:
        page = page.getRedirectTarget()
    except:
        pass
    title = page.title()
    print(title)
    if title in page_titles:
        return page_titles
    if page.namespace() not in (0,14,100,108,):
        return page_titles
    else:
        page_titles.add(page.title())
        if (len(page_titles)>max_pages):
            raise ValueError("MAX DEPTH REACHED")
        if (depth>max_depth):
            return page_titles
        for subpage in page.linkedPages(total = max_pages//4):
            page_titles = pull(subpage, page_titles, max_pages, depth+1, max_depth)
        for superpage in page.getReferences(total = max_pages//4):
            page_titles = pull(superpage, page_titles, max_pages, depth+1, max_depth)
    return page_titles

wordlist = []

with open('words.json','r') as f:
    datastore=json.load(f)

for r in range(0,len(datastore[0])-1):
    #print(datastore[0]["WORD"+str(r+1)].lower())
    wordlist.append(datastore[0]["WORD"+str(r+1)].lower().replace(" ", "_"))

#print(wordlist)

try:
    os.mkdir("corpora")
    os.chdir("corpora")
except OSError:
    os.chdir("corpora")

banlist = []
for word in wordlist:
    if not os.path.isfile(str(word+".json")):
        print(word)
        banlist.append(word)

for word in banlist:
    #print(word)
    page_titles = set()
    page = pywikibot.Page(site, word)
    try:
        page = page.getRedirectTarget()
    except:
        pass
    try:
        page_titles = pull(page, page_titles, 10000,0,1)
    except ValueError:
        #print (e.message)
        pass
    except:
        break
    print(word+" sEaRcHeD sUcCeSsFuLlY")
    f = open(word+".json",'w')
    word_titles = list(page_titles)
    json.dump(word_titles, f)
    f.close()
"""

word = "new_york"
page_titles = set()
try:
    page_titles = func_timeout(100, pull, args=(pywikibot.Page(site, word), page_titles, 10000,0,1), kwargs=None)
except ValueError as e:
    #print (e.message)
    pass
except FunctionTimedOut:
    print(word + " skipped because timeout")
except:
    print (word+" SKIPPED BECAUSE OTHER REASONS")
"""

ny = pywikibot.Page(site, "new_york")
try:
    ny = ny.getRedirectTarget()
except:
    print("ERROR")
print(ny.text)
#print("done")