import json
import random
import nltk
from nltk.corpus import wordnet as wn
import itertools

class Pair:
    #sim = 0
    #word = ""
    #word2 = ""
    
    def __init__(self, sim, word, word2):
        self.sim = sim
        self.word = word
        self.word2 = word2
        self.hyper = []
        self.hypo = []
        self.root = []
        self.common = []
        self.memholo = []
        self.hyper2 = []
        self.hypo2 = []
        self.root2 = []
        self.common2 = []
        self.memholo2 = []
        self.megac = []
        self.lemsc = []
        self.totalc = []
        self.cat = []
        self.cat2 = []
        self.inhypo = []
        self.inhyper = []
        self.inhypo2 = []
        self.inhyper2 = []
        self.memmero = []
        self.submero = []
        self.partmero = []
        self.topic = []
        self.region = []
        self.usage = []
        self.cause = []
        self.sims = []
        self.subholo = []
        self.partholo = []
        self.memmero2 = []
        self.submero2 = []
        self.partmero2 = []
        self.topic2 = []
        self.region2 = []
        self.usage2 = []
        self.cause2 = []
        self.sims2 = []
        self.partholo2 = []
        self.subholo2 = []
        self.lems = []
        self.lems2 = []
        
    def __repr__(self):
        return '{}: {} {} {}'.format(self.__class__.__name__,
                                  self.word,
                                  self.word2,
                                  self.sim)
    def getSets(self):
        for synset in wn.synsets(self.word):
            self.cat.append(synset.lexname())
            try:
                #print("TEST: "+self.word)
                #print(synset.hypernyms())
                res = synset.hypernyms()[0].lemma_names()
                self.hyper += res
            except:
                pass
            try:
                res = synset.hyponyms()[0].lemma_names()
                self.hypo += res
            except:
                pass
            try:
                res = synset.root_hypernyms()[0].lemma_names()
                self.root += res
            except:
                pass
            try:
                res = synset.lowest_common_hypernyms()[0].lemma_names()
                self.common += res
            except:
                pass
            try:
                res = synset.member_holonyms()[0].lemma_names()
                self.memholo += res
            except:
                pass
            try:
                res = synset.instance_hypernyms()[0].lemma_names()
                self.inhyper += res
            except:
                pass
            try:
                res = synset.instance_hyponyms()[0].lemma_names()
                self.inhypo += res
            except:
                pass
            try:
                res = synset.substance_holonyms()[0].lemma_names()
                self.subholo += res
            except:
                pass
            try:
                res = synset.part_holonyms()[0].lemma_names()
                self.partholo += res
            except:
                pass
            try:
                res = synset.member_meronyms()[0].lemma_names()
                self.memmero += res
            except:
                pass
            try:
                res = synset.substance_meronyms()[0].lemma_names()
                self.submero += res
            except:
                pass
            try:
                res = synset.part_meronyms()[0].lemma_names()
                self.partmero += res
            except:
                pass
            try:
                res = synset.topic_domains()[0].lemma_names()
                self.topic += res
            except:
                pass
            try:
                res = synset.region_domains()[0].lemma_names()
                self.region += res
            except:
                pass
            try:
                res = synset.usage_domains()[0].lemma_names()
                self.usage += res
            except:
                pass
            try:
                res = synset.causes()[0].lemma_names()
                self.cause += res
            except:
                pass
            try:
                res = synset.similar_tos()[0].lemma_names()
                self.sims += res
            except:
                pass
            try:
                res = synset.lemma_names()
                self.lems += res
            except:
                pass
        for synset in wn.synsets(self.word2):
            self.cat2.append(synset.lexname())
            try:
                #print("TEST: "+self.word2)
                #print(synset.hypernyms())
                res = synset.hypernyms()[0].lemma_names()
                self.hyper2 += res
            except:
                pass
            try:
                res = synset.hyponyms()[0].lemma_names()
                self.hypo2 += res
            except:
                pass
            try:
                res = synset.root_hypernyms()[0].lemma_names()
                self.root2 += res
            except:
                pass
            try:
                res = synset.lowest_common_hypernyms()[0].lemma_names()
                self.common2 += res
            except:
                pass
            try:
                res = synset.member_holonyms()[0].lemma_names()
                self.memholo2 += res
            except:
                pass
            try:
                res = synset.instance_hypernyms()[0].lemma_names()
                self.inhyper2 += res
            except:
                pass
            try:
                res = synset.instance_hyponyms()[0].lemma_names()
                self.inhypo2 += res
            except:
                pass
            try:
                res = synset.substance_holonyms()[0].lemma_names()
                self.subholo2 += res
            except:
                pass
            try:
                res = synset.part_holonyms()[0].lemma_names()
                self.partholo2 += res
            except:
                pass
            try:
                res = synset.member_meronyms()[0].lemma_names()
                self.memmero2 += res
            except:
                pass
            try:
                res = synset.substance_meronyms()[0].lemma_names()
                self.submero2 += res
            except:
                pass
            try:
                res = synset.part_meronyms()[0].lemma_names()
                self.partmero2 += res
            except:
                pass
            try:
                res = synset.topic_domains()[0].lemma_names()
                self.topic2 += res
            except:
                pass
            try:
                res = synset.region_domains()[0].lemma_names()
                self.region2 += res
            except:
                pass
            try:
                res = synset.usage_domains()[0].lemma_names()
                self.usage2 += res
            except:
                pass
            try:
                res = synset.causes()[0].lemma_names()
                self.cause2 += res
            except:
                pass
            try:
                res = synset.similar_tos()[0].lemma_names()
                self.sims2 += res
            except:
                pass
            try:
                res = synset.lemma_names()
                self.lems2 += res
            except:
                pass
        """self.hyperc = list(set(self.hyper) & set(self.hyper2))
        self.hypoc = list(set(self.hypo) & set(self.hypo2))
        self.memberc = list(set(self.member) & set(self.member2))
        self.commonc = list(set(self.common) & set(self.common2))
        self.rootc = list(set(self.root) & set(self.root2))"""
        self.megac = list(set(self.root+self.hyper+self.hypo+self.memholo+\
                              self.common+self.cat+self.inhypo+self.inhyper+\
                              self.subholo+self.partholo+self.memmero+self.submero+\
                              self.partmero+self.topic+self.region+self.usage+\
                              self.cause+self.sims)\
                          & set(self.root2+self.hyper2+self.hypo2+self.memholo2+\
                                self.common2+self.cat2+self.inhypo2+self.inhyper2+\
                                self.subholo2+self.partholo2+self.memmero2+self.submero2+\
                                self.partmero2+self.topic2+self.region2+self.usage2+\
                                self.cause2+self.sims2))
        self.lemsc = list(set(self.lems) & set(self.lems2))
        self.totalc = list(set(self.megac + self.lemsc))
        
        

def getKey(pair):
    return pair.sim

def run():
    with open('words.json','r') as f:
        datastore=json.load(f)
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

    print("Assassin = "+assassin)
    
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
    #print("assassin hyponyms")
    #print(wn.synsets(assassin)[0].hyponyms()[0].lemma_names())
    
    tem = Pair(0, "test", "test")
    best = [tem,tem,tem,tem,tem]

    combs = list(itertools.combinations(redwords,2))
    print("dbshdvewugcde")
    print(combs)
    print(combs[0][0])
    
    for tup in combs:
        word = tup[0]
        word2= tup[1]
        print("\n"+word+" SIMILARITY TO "+word2)
        try:
            res = wn.synsets(word2)[0].wup_similarity(wn.synsets(word)[0])
        except:
            continue
        pair = Pair(res,word,word2)
        print(res)
        print(best[0])
        if res> (best[0]).sim:
            best[0] = pair
            best = sorted(best, key=getKey)
    print(best)
            
    pair1 = best[4]
    pair2 = best[3]
    pair3 = best[2]
    pair1.getSets()
    pair2.getSets()
    pair3.getSets()
    print (pair1.lems)
    
    def pairPrint(pair):
        print("Word: "+pair.word+" + Word2: "+pair.word2+" COMMON RELATED WORDS\n")
        #print(pair.hyperc)
        #print(pair.hypoc)
        #print(pair.rootc)
        #print(pair.commonc)
        #print(pair.memberc)
        #print(pair.catc)
        print(pair.megac)
        print(pair.lemsc)
        print(pair.totalc)
    
    pairPrint(pair1)
    pairPrint(pair2)
    pairPrint(pair3)
        
    for word in redwords:
        #print("\nBEGINNING WORD === "+word+" ===\n")
        for synset in wn.synsets(word):
           #print(synset)
            #for lemma in synset.lemmas():
                #print(lemma.name())
            try:
                res = synset.hypernyms()[0].lemma_names()
                #print("HYPERNYMS")
                #print(res)
            except:
                #print("NO HYPERNYMS")
                pass
            try:
                res = synset.hyponyms()[0].lemma_names()
                #print("HYPONYMS")
                #print(res)
            except:
                #print("NO HYPONYMS")
                pass
            try:
                res = synset.root_hypernyms()[0].lemma_names()
                #print("ROOT HYPERNYMS")
                #print(res)
            except:
                #print("NO ROOT HYPERNYMS")
                pass
            try:
                res = synset.lowest_common_hypernyms()[0].lemma_names()
                #print("LOWEST COMMON HYPERNYMS")
                #print(res)
            except:
                #print("NO LOWEST COMMON HYPERNYMS")
                pass
            try:
                res = synset.member_holonyms()[0].lemma_names()
                #print("MEMBER HOLONYMS")
                #print(res)
            except:
                #print("NO HOLONYMS")
                pass
    """print("assassin hypernyms")
    print(wn.synsets(assassin)[0].hypernyms()[0].lemma_names())
    print("assassin member holonyms")
    print(wn.synsets(assassin)[0].member_holonyms()[0].lemma_names())
    print("assassin meronyms")
    print(wn.synsets(assassin)[0].meronyms()[0].lemma_names())
    print("assassin troponyms")
    print(wn.synsets(assassin)[0].troponyms()[0].lemma_names())

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
    """
    
run()

