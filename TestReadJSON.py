import json
import random
import requests

def syn_func(subject):
    app_id = 'a280a009'
    app_key = '9c95a03ce17f391af63caf92c9b9abb7'
    language = 'en'
    word_id = subject
    print(word_id)
    url = "https://od-api.oxforddictionaries.com:443/api/v1/entries/"+language+"/"+word_id.lower()+"/synonyms"
    r=requests.get(url, headers={'app_id' : app_id, 'app_key' : app_key})
    try:
        data = r.json()
        syns = []
        for d in data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["synonyms"]:
            #print(d["id"])
            syns.append(d["id"])
        return syns
    except:
        print("NONE FOUND")
        return []
    
with open('words.json','r') as f:
    datastore=json.load(f)
random.seed()
n = 0;
wordset = []
for i in range(25):
    r = random.randint(0,len(datastore[0])-1)
    print("|"+datastore[0]["WORD"+str(r+1)]+"|", end="")
    wordset.append(datastore[0]["WORD"+str(r+1)])
    n+=1
    if n>=5:
        print("\n")
        n=0

syn_func(datastore[0]["WORD"+str(r+1)])

r2 = random.randint(0,1)

redwords = []
bluewords = []
bywords = []
wordset_copy = wordset

if (r2>0):
    first = "red"
    extra = wordset[random.randint(0,25)]
    redwords.append(extra)
    wordset_copy.remove(extra)
else:
    first = "blue"
    extra = wordset[random.randint(0,25)]
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
    
print("\nred")
print(redwords)
print("blue")
print(bluewords)
print("bystanders")
print(bywords)
print("assassin")
print(assassin+"\n")

for w in redwords:
    base = syn_func(w)
    print(base)
