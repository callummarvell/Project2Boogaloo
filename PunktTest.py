# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 12:24:39 2018

@author: Callum Marvell
"""
import json
import random
import nltk
from gensim.models import Word2Vec, KeyedVectors
from nltk.corpus import brown
from nltk.corpus import gutenberg
from nltk.corpus import abc
from nltk.corpus import genesis
from nltk.corpus import subjectivity
import wikipedia

reload_model = False
tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
wordlist = []
pages = ""
    
with open('words.json','r') as f:
    datastore=json.load(f)

def get_wiki(word):
    global pages
    try:
        pages += wikipedia.page(word).content
    except:
        pass

try:
    if reload_model==True:
        raise Exception('Flag set, reloading model')
    g = KeyedVectors.load_word2vec_format('./model.bin', binary=True)
except:
    """with open('words.json','r') as f:
        datastore=json.load(f)
    random.seed()
    pages = ""
    for word in datastore[0]:
        pages += wikipedia.page(word).content
    """
    for r in range(0,len(datastore[0])-1):
        #print(datastore[0]["WORD"+str(r+1)].lower())
        wordlist.append(datastore[0]["WORD"+str(r+1)].lower())
    for word in wordlist:
        try:
            for thing in wikipedia.search(word):
                #print("SEARCH TERM: "+thing)
                #print(wikipedia.page(thing))
                #print(wikipedia.page(thing).content)
                pages += wikipedia.page(thing).content
        except wikipedia.DisambiguationError as e:
            s = random.choice(e.options)
            get_wiki(s)
            pass
        except:
            pass
    b = brown.sents()
    sents = tokenizer.tokenize(pages)
    sense = gutenberg.sents('austen-sense.txt')
    emma = gutenberg.sents('austen-emma.txt')
    persuasion = gutenberg.sents('austen-persuasion.txt')
    bible = genesis.sents('english-kjv.txt')
    blake = gutenberg.sents('blake-poems.txt')
    bryant = gutenberg.sents('bryant-stories.txt')
    burgess= gutenberg.sents('burgess-busterbrown.txt')
    carroll = gutenberg.sents('carroll-alice.txt')
    ch_ball = gutenberg.sents('chesterton-ball.txt')
    ch_brown = gutenberg.sents('chesterton-brown.txt')
    ch_thurs = gutenberg.sents('chesterton-thursday.txt')
    edge = gutenberg.sents('edgeworth-parents.txt')
    mel = gutenberg.sents('melville-moby_dick.txt')
    mil = gutenberg.sents('milton-paradise.txt')
    caesar = gutenberg.sents('shakespeare-caesar.txt')
    hamlet = gutenberg.sents('shakespeare-hamlet.txt')
    macbeth = gutenberg.sents('shakespeare-macbeth.txt')
    whit = gutenberg.sents('whitman-leaves.txt')
    rural = abc.sents('rural.txt')
    science = abc.sents('science.txt')
    plots = subjectivity.sents('plot.tok.gt9.5000')
    quotes = subjectivity.sents('quote.tok.gt9.5000')
    austen = sense+emma+persuasion
    shakespeare = caesar+hamlet+macbeth
    facts = rural+science
    opinions = plots+quotes
    gute = bryant+burgess+carroll+edge+mel+mil+whit
    chester = ch_ball+ch_brown+ch_thurs
    total = austen+shakespeare+facts+opinions+gute+chester+b+sents
    #print(plots)
    #print(science)
    #print(bible)
    g = Word2Vec(total)
    g.wv.save_word2vec_format('model.bin', binary=True)

def run():
    random.seed()
    n = 0;
    wordset = []
    for i in range(25):
        r = random.randint(0,len(datastore[0])-1)
        print("|"+datastore[0]["WORD"+str(r+1)].lower()+"|", end="")
        wordset.append(datastore[0]["WORD"+str(r+1)].lower())
        n+=1
        if n>=5:
            print("\n")
            n=0

    #syn_func(datastore[0]["WORD"+str(r+1)])

    r2 = random.randint(0,1)

    redwords = []
    bluewords = []
    bywords = []
    wordset_copy = wordset.copy()

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

    print("Assassin = "+assassin)
    #print(g.most_similar("money", topn=5))
    for word in wordset:
        try:
            #pag = wikipedia.page(word)
            print("WORD= "+word)
            print(g.most_similar(word, topn=5))
            #print(pag.content)
            #print(pag.section(pag.sections[0]))
        except:
            print(word+" word is not known")
    
    current=1-redfirst

    def turn(team):
        ass = False
        if (team==0):
            print("IT IS YOUR TURN, TEAM RED\n")
            num = int(input("RED SPYMASTER, how many words are you connecting? "))
            input("RED SPYMASTER, what is your clue? ")
            for i in range(0,num+1):
                if (len(redwords)==0):
                    return ass
                guess = input("RED TEAM, enter a guess for the clue ")
                if (guess.lower()=="endturn"):
                    print("You have ended your turn, RED TEAM")
                    return ass
                try:
                    redwords.index(guess.lower())
                    print("CORRECT, that was one of your team's words")
                    redwords.remove(guess.lower())
                except:
                    if (assassin==guess):
                        actual="THE ASSASSIN"
                        ass=True
                    else:
                        try:
                            bluewords.index(guess.lower())
                            actual="one of the BLUE TEAM'S WORDS"
                            bluewords.remove(guess.lower())
                        except:
                            try:
                                bywords.index(guess.lower())
                                actual="one of the BYSTANDERS"
                                bywords.remove(guess.lower())
                            except:
                                print("ERROR")
                                actual = "ERROR"
                    print("INCORRECT, "+guess+" was "+actual)
                    return ass
            print("RED TEAM, you are out of guesses, good job!")
        else:
            print("IT IS YOUR TURN, TEAM BLUE\n")
            num = int(input("BLUE SPYMASTER, how many words are you connecting? "))
            input("BLUE SPYMASTER, what is your clue? ")
            for i in range(0,num+1):
                if (len(redwords)==0):
                    return ass
                guess = input("BLUE TEAM, enter a guess for the clue ")
                if (guess.lower()=="endturn"):
                    print("You have ended your turn, BLUE TEAM")
                    return ass
                try:
                    bluewords.index(guess.lower())
                    print("CORRECT, that was one of your team's words")
                    bluewords.remove(guess.lower())
                except:
                    if (assassin==guess):
                        actual="THE ASSASSIN"
                        ass=True
                    else:
                        try:
                            redwords.index(guess.lower())
                            actual="one of the RED TEAM'S WORDS"
                            redwords.remove(guess.lower())
                        except:
                            try:
                                bywords.index(guess.lower())
                                actual="one of the BYSTANDERS"
                                bywords.remove(guess.lower())
                            except:
                                print("ERROR")
                                actual="ERROR"
                    print("INCORRECT, "+guess+" was "+actual)
                    return ass
            print("BLUE TEAM, you are out of guesses, good job!")
        
    def win(team):
        if (team==1):
            print("BLUE TEAM WINS!!!!")
        else:
            print("RED TEAM WINS!!!!")
        again = input("PLAY AGAIN? Y/N: ")
        if (again.lower()=="y"):
            print("Setting up another game!")
            print("========================\n")
            run()
        else:
            print("Thanks for playing!")

    print("\nred")
    print(redwords)
    print("blue")
    print(bluewords)
    print("bystanders")
    print(bywords)
    print("assassin")
    print(assassin+"\n")

    dead=False
    while (len(redwords)>0 and len(bluewords)>0 and dead!=True):
        dead = turn(current)
        current=1-current
    if (dead==True):
        win(current)
    elif (len(bluewords)==0):
        win(1)
    else:
        win(0)
    
run()