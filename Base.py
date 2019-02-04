import json
import random

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
        extra = wordset[random.randint(0,25)]
        redwords.append(extra)
        wordset_copy.remove(extra)
    else:
        redfirst = 0
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