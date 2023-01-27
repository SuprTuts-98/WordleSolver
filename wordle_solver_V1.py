import random
from os import system, name
import os
import csv

with open('commonFiveLetter.csv') as c:
    common=[tuple(line) for line in csv.reader(c)]
c.close()

original_file = "wordle_words.txt"
temp_file = "temp.txt"

def clear_screen():
		if name == 'nt':
			_ = system('cls')
		else:
			_ = system('clear')
            
board = [
[" ", " ", " ", " ", " "],
[" ", " ", " ", " ", " "],
[" ", " ", " ", " ", " "],
[" ", " ", " ", " ", " "],
[" ", " ", " ", " ", " "],
[" ", " ", " ", " ", " "],
]

startingWords = ["SOARE", "SAREE", "SEARE", "STARE", "ROATE"]

def print_board():
	clear_screen()
	for r in board:
		print (*r)
    
def validInput(w):
    return len(w) == 5
        
def convert(s):
    new = ""
    for x in s:
        new += x
    return new
 
def solver():
    fiveLetterWords = set(open('wordle_words.txt').read().upper().split())
    initialInput = input("Would you like me to provide a starting word?")
    startingWord = 0
    if "y" in initialInput.lower():
        startingWord = random.choice(startingWords)
    elif "n" in initialInput.lower():
        while True:
            userWord = input("What was your starting word?")
            if validInput(userWord) == True:
                startingWord = userWord.upper()
                break
            else:
                print ("Invalid word length")
    else:
        print("Invalid answer")
        
    board[0][0] = startingWord[0]
    board[0][1] = startingWord[1]
    board[0][2] = startingWord[2]
    board[0][3] = startingWord[3]
    board[0][4] = startingWord[4]
    
    moveCount = 0
    currentWord = [*startingWord]
    while True:
        print_board()
        print("Enter 'G' to generate a new word \nUse Y to represent present letters in the right spot, \nN to represent absent letters, \nand W to represent present letters in the wrong spot")
        results = input().upper()
        print("E.G. NNYWW")
        currentResult = [*results]
        tempWordSet = fiveLetterWords.copy()
        contains = []
        containsIndex = []
        wrongSpot = []
        wrongSpotIndex = []
        absent = []
        sortaAbsent = []
        sortaAbsentIndex = []
        if "G" in currentResult:
            string_to_delete = [convert(currentWord)]
            with open(original_file, "r") as inputT:
                with open(temp_file, "w") as output:
                    for line in inputT:
                        for wordT in string_to_delete:
                            line = line.replace(wordT, "")
                        output.write(line)
            os.replace('temp.txt', 'wordle_words.txt')
            currentWord = [*fiveLetterWords.pop()]
            moveCount -= 1
        else:
            for j in range(0, 5):
                if currentResult[j] == "Y":
                        contains.append(currentWord[j])
                        containsIndex.append(j)
            for i in range(0, 5):
                if currentResult[i] == "W":
                    wrongSpot.append(currentWord[i])
                    wrongSpotIndex.append(i)
                elif currentResult[i] == "N" and (currentWord[i] in contains or currentWord[i] in wrongSpot):
                    sortaAbsent.append(currentWord[i])
                    sortaAbsentIndex.append(i)
                elif currentResult[i] == "N" and (currentWord[i] not in contains and currentWord[i] not in wrongSpot):
                    absent.append(currentWord[i])
            if contains:
                for lettersY in range(len(contains)):
                    tempWordSet = {wordY for wordY in tempWordSet if contains[lettersY] in wordY and contains[lettersY] == wordY[int(containsIndex[lettersY])]}
            if wrongSpot:
                for lettersW in range(len(wrongSpot)):
                    if wrongSpot[lettersW] in contains:
                        tempWordSet = {wordW for wordW in tempWordSet if wrongSpot[lettersW] in wordW and wrongSpot[lettersW] != wordW[int(wrongSpotIndex[lettersW])] and wordW.count(wrongSpot[lettersW]) > 1}
                    else:
                        tempWordSet = {wordW for wordW in tempWordSet if wrongSpot[lettersW] in wordW and wrongSpot[lettersW] != wordW[int(wrongSpotIndex[lettersW])]}
            if sortaAbsent:
                for lettersSN in range(len(sortaAbsent)):
                    tempWordSet = {wordSN for wordSN in tempWordSet if sortaAbsent[lettersSN] in wordSN and sortaAbsent[lettersSN] != wordSN[int(sortaAbsentIndex[lettersSN])]}           
            if absent:
                for lettersN in range(len(absent)):
                    tempWordSet = {wordN for wordN in tempWordSet if absent[lettersN] not in wordN}
        moveCount += 1
        fiveLetterWords = tempWordSet
        tempIntersect = []
        for pair in common:
            if pair[0].upper() in fiveLetterWords:
                tempIntersect.append(pair)
        if tempIntersect:
            highest = 0
            highestWord = 0
            for pairI in tempIntersect:
                if int(pairI[1]) > int(highest):
                    highest = pairI[1]
                    highestWord = pairI[0].upper()
            currentWord = [*highestWord]
        else:
            currentWord = [*fiveLetterWords.pop()]
        board[moveCount][0] = currentWord[0]
        board[moveCount][1] = currentWord[1]
        board[moveCount][2] = currentWord[2]
        board[moveCount][3] = currentWord[3]
        board[moveCount][4] = currentWord[4]

while True:
    solver()