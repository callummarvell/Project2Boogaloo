# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 14:28:56 2019

@author: callu
"""
def turn(team):
    if (team==0):
        print("IT IS YOUR TURN, TEAM RED\n")
        num = int(input("RED SPYMASTER, how many words are you connecting? "))
        clue = input("RED SPYMASTER, what is your clue?")
        return (num,clue)
    else:
        print("IT IS YOUR TURN, TEAM BLUE\n")
        num = int(input("BLUE SPYMASTER, how many words are you connecting? "))
        clue = input("BLUE SPYMASTER, what is your clue? ")
        return (num,clue)
        
def checkGuess(team, guess, redwords, bluewords, bywords, assassin):
    ass = False
    wrong = False
    if team == 0:
        if (guess.lower()=="endturn"):
            print("You have ended your turn, RED TEAM")
            return ass, wrong
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
                    wrong = True
                except:
                    try:
                        bywords.index(guess.lower())
                        actual="one of the BYSTANDERS"
                        bywords.remove(guess.lower())
                        wrong = True
                    except:
                        print("ERROR")
                        actual = "ERROR"
            print("INCORRECT, "+guess+" was "+actual)
            return ass, wrong
    else:
        if (guess.lower()=="endturn"):
            print("You have ended your turn, BLUE TEAM")
            return ass, wrong
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
                    wrong = True
                except:
                    try:
                        bywords.index(guess.lower())
                        actual="one of the BYSTANDERS"
                        bywords.remove(guess.lower())
                        wrong = True
                    except:
                        print("ERROR")
                        actual = "ERROR"
            print("INCORRECT, "+guess+" was "+actual)
            return ass, wrong
    return ass, wrong
        
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