# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 14:04:45 2020

@author: Raúl
"""
import copy

class Jolka:
    
    #variables to hold the state of the board and the words remaining
    #unused for the current state of the game
    boardSetup = []
    wordList = []

    #constructor for the Jolka class, assigning it an initial board
    #setup and a list of available words    
    def __init__(self,boardSetup,wordList):
        self.boardSetup = boardSetup
        self.wordList = wordList
            
    #function that checks whether the game is finished (every cell has a char.)
    def isGameFinished(self):
        if len(self.wordList) == 0:
            return True
        for i in range(len(self.boardSetup)):
                for j in range(len(self.boardSetup[0])):
                    if self.boardSetup[i][j] != "#":
                        if self.boardSetup[i][j][0] == "_":
                            return False 
        return True
    
    #function to mark the positions where a word begins 
    #it also marks duplicated starting points (both a vertical and a horizontal
    #word start in that same cell)
    def findStartingPositions(self):
        heightBoard = len(self.boardSetup)
        widthBoard = len(self.boardSetup[0])
        listOfStartingPositions = []
        for i in range(heightBoard):
            for j in range(len(self.boardSetup[i])):
                if self.boardSetup[i][j][0] != "#":
                #cases for the borders (i == 0 and j == 0)
                    if i == 0 and self.boardSetup[i+1][j] != "#":
                        self.boardSetup[i][j][2] = "T"
                        listOfStartingPositions.append([i,j])
                        if j+1 < widthBoard:
                            if self.boardSetup[i][j+1] != "#" and j==0:
                                self.boardSetup[i][j][1] = "T"
                    elif j == 0 and self.boardSetup[i][j+1] != "#":
                        self.boardSetup[i][j][1] = "T"
                        listOfStartingPositions.append([i,j])
                   #cases for words in the middle or not the extremes
                    elif j < widthBoard-1 and self.boardSetup[i][j+1] != "#" and self.boardSetup[i][j-1] == "#":
                        self.boardSetup[i][j][1]= "T"
                        listOfStartingPositions.append([i,j])
                    elif i < heightBoard-1 and self.boardSetup[i+1][j] != "#" and self.boardSetup[i-1][j] == "#":
                        self.boardSetup[i][j][2] = "T"
                        listOfStartingPositions.append([i,j])
        return listOfStartingPositions
    
    #function that finds out the horizontal and vertical domain for the blank
    #spaces in the board, taking into account the length of the blank and
    #the remaining words on the list
    def findDomainAvailableWords(self):
         heightBoard = len(self.boardSetup)
         widthBoard = len(self.boardSetup[0])
         domainVertical = []
         domainHorizontal = []
         #we traverse the board
         for i in range(heightBoard):
             for j in range(len(self.boardSetup[i])):
                 #if we found a starting position for a word we have to find 
                 #out the length of the word or words
                 if self.boardSetup[i][j][0] != "#" and self.boardSetup[i][j][1] == "T":
                         counterHorizontal = 0
                         #we continue going right and update the counter
                         #to register the length of the word
                         while j < widthBoard -1 and self.boardSetup[i][j+counterHorizontal] != "#":
                                 counterHorizontal+=1
                                 if j+counterHorizontal == widthBoard:
                                     break
                         #we iterate over the words left
                         for word in self.wordList:
                             #when we find a word with the correct length we
                             #add it to the corresponding domain
                             if len(word) == counterHorizontal:
                                 domainHorizontal.append(word)
                         #finally, we store both domains in their respective
                         #list inside the board cell
                         self.boardSetup[i][j][3]= domainHorizontal
                        
                 if self.boardSetup[i][j][0] != "#" and self.boardSetup[i][j][2] == "T":
                         counterVertical= 0
                         #we continue going down and update the counter
                         #to register the length of the word
                         while i < heightBoard -1 and self.boardSetup[i+counterVertical][j] != "#":
                                 counterVertical+=1
                                 if i+counterVertical == heightBoard:
                                     break
                         #we iterate over the words left
                         for word in self.wordList:
                             if len(word) == counterVertical:
                                 domainVertical.append(word)
                         self.boardSetup[i][j][4]= domainVertical
                 #we empty the domains in order to continue iterating to the 
                 #next cell
                 domainHorizontal = []
                 domainVertical = []
         return self
        
    #function that analyzes and alters the domain of the board based on the
    #words already present in it, keeping the constraints in place
    def findDomainCrossingWords(self, startingPositions):
        #quizás meter un starting extra, uno pa htal y otro pa vcal
        #iterate over all the starting positions
        #iterate over the domain so far
        #try to see if the domain fits when they cross to a column
        #check if the character is right
        for position in startingPositions:
            startForCurrentWord = self.boardSetup[position[0]][position[1]]
            #we check if the start is horizontal
            if startForCurrentWord[1] == "T":
                #copy needed in order to alter only that one and keep the
                #for in loop working correctly
                copyOfHDomain = copy.deepcopy(startForCurrentWord[3])
                for wordInHorizontalDomain in startForCurrentWord[3]:
                    lengthToCheck = len(wordInHorizontalDomain)
                    wordCanBeFilled = True
                    k = 0
                    while k in range(lengthToCheck) and wordCanBeFilled:
                        characterToCompare = wordInHorizontalDomain[k]
                        charOccupying = self.boardSetup[position[0]][position[1]+k][0]
                        if charOccupying != "_" and charOccupying != characterToCompare:
                            wordCanBeFilled = False
                        k+=1
                    #if the word cannot fit because it would mess another
                    #we delete it from the horizontal domain
                    if wordCanBeFilled == False:
                        copyOfHDomain.remove(wordInHorizontalDomain)
                #if after this check the horizontal domain is empty
                #we must update the flag
                if len(startForCurrentWord[3]) == 0:
                    startForCurrentWord[1] = "F"
                startForCurrentWord[3] = copyOfHDomain
            #we check if the start is vertical (could be both)
            if startForCurrentWord[2] == "T":
                copyOfVDomain = copy.deepcopy(startForCurrentWord[4])
                for wordInVerticalDomain in startForCurrentWord[4]:
                    lengthToCheck = len(wordInVerticalDomain)
                    wordCanBeFilled = True
                    k = 0
                    while k in range(lengthToCheck) and wordCanBeFilled:
                        characterToCompare = wordInVerticalDomain[k]
                        charOccupying = self.boardSetup[position[0]+k][position[1]][0]
                        if charOccupying != "_" and charOccupying != characterToCompare:
                            wordCanBeFilled = False
                        k+=1
                    #if the word cannot fit because it would mess another
                    #we delete it from the horizontal domain
                    if wordCanBeFilled == False:
                        copyOfVDomain.remove(wordInVerticalDomain)
                #if after this check the horizontal domain is empty
                #we must update the flag
                if len(startForCurrentWord[4]) == 0:
                    startForCurrentWord[1] = "F"
                startForCurrentWord[4] = copyOfVDomain
        return self
    
    #function that displays the state of the board, mainly for displaying 
    #the solutions found and also for debugging purposes
    def printSimplifiedBoard(self):
        for i in range(len(self.boardSetup)):
            for j in range(len(self.boardSetup[i])):
               if j == 0:
                   print("\n")
               if self.boardSetup[i][j] == "#":
                   print(self.boardSetup[i][j][0], end=" ")
               else:
                   print(self.boardSetup[i][j][0], end = " ")
                   #print(self.boardSetup[i][j][1], end = " ")
                   #print("\n")
        print("\n")
        print("\n")
        
    
    #function to find the minimum domain from the list of starting positions
    def findMinimumDomain(self, listOfStartingPositions):
        minimumDomain = 200
        minimumPosition = ['','']
        #we iterate over the positions and swap the min. value and position
        #when we find a lower value
        for position in listOfStartingPositions:
            numberOfHorizontalWords = 0
            numberOfVerticalWords = 0
            cell = self.boardSetup[position[0]][position[1]]
            if cell[1] == "T" or cell[2] == "T":
                    if cell[1] == "T":
                        numberOfHorizontalWords = len(cell[3])
                    if cell[2] == "T":
                        numberOfVerticalWords = len(cell[4])
            else:
                continue
            totalWords = numberOfHorizontalWords + numberOfVerticalWords
            if totalWords < minimumDomain:
                minimumDomain = totalWords
                minimumPosition = position
        return minimumPosition
    
    #function that inserts a given word into a position on the board
    #taking into account the orientation flag
    def insertWordInPosition(self,word,positionX,positionY,orientation):
        if orientation == "H":
            for i in range(len(word)):
                self.boardSetup[positionX][positionY+i][0] = word[i]
            if word in self.wordList:
                self.wordList.remove(word)
            self.boardSetup[positionX][positionY][3] = []
            #change the flag value for the starting position, now that it 
            #has a horizontal word it no longer can be considered as a 
            #posibility for another one of that kind
            self.boardSetup[positionX][positionY][1] = "F"
        else:
            for i in range(len(word)):
                self.boardSetup[positionX+i][positionY][0] = word[i]
            if word in self.wordList:
                self.wordList.remove(word)
            self.findDomainAvailableWords()
            self.boardSetup[positionX][positionY][4] = []
            #change the flag value for the starting position, now that it 
            #has a word it no longer can be considered as a posibility
            #for another vertical word
            self.boardSetup[positionX][positionY][2] = "F"
        return self

    
    #check if the domain of any of the starting positions has words left
    #otherwise the current development of the board is wrong
    def isCrosswordSolvable(self, positionsOfStart):
        for position in positionsOfStart:
            if self.boardSetup[position[0]][position[1]][3] is None and self.boardSetup[position[0]][position[1]][4] is None:
                return False
        return True