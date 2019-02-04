import csv
import random
from PyDictionary import PyDictionary

dictionary=PyDictionary()

with open('words.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
random.seed()
n = 0;
for i in range(25):
    r = random.randint(0,len(data[0])-1)
    print("|"+data[0][r]+"|", end="")
    n+=1
    if n>=5:
        print("\n")
        n=0
print(dictionary.synonym("Life"))
