# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 14:28:56 2019

@author: callu
"""
def turn(team, redwords, bluewords, bywords, assassin):
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
        return True
    else:
        print("Thanks for playing!")
        return False
    
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