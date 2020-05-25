# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 14:05:01 2020

@author: Raúl
"""
from Jolka import Jolka
import copy
import time

#function that splits a string in its individual characters
#useful in get_sudokus() to split the original sudoku layout
def split_in_chars(word): 
        return [char for char in word]  
    
class fillInCSP:
    #variable to store the words for a given word file
    wordList = []
    boardSetup = []
    
    #flag to stop the tree from growing once a solution has been found
    solutionFound = False
    
    def __init__(self,fileBoard,fileWords):
        self.fileBoard = fileBoard
        self.fileWords = fileWords
        self.boardSetup = self.loadBoard(fileBoard)
        self.loadWords(fileWords)
   
    #function that loads the board layout from the file provided
    #marking each square as empty or not valid (# symbol in the file)
    def loadBoard(self,fileBoard):
        boardFile = open(fileBoard,"r")
        listOfLinesFromBoard = []
        for line in boardFile:
            #slice needed to delete the \n character appearing on some files
            line = line[:-1]
            line = split_in_chars(line)
            lineWithState = []
            for ch in line:
                if ch == "_":
                    ch = [ch,"F","F",None,None]
                lineWithState.append(ch)
            listOfLinesFromBoard.append(lineWithState)
        return listOfLinesFromBoard
    
    
    #function to load words from the file provided
    def loadWords(self,fileWords):
        wordsFile = open(fileWords,"r")
        for line in wordsFile:
            #slice needed to delete the \n character appearing on some files
            line = line[:-1]
            self.wordList.append(line)
            

    def run(self):
        jolkaSolver = Jolka(self.boardSetup, self.wordList)
        startingPositions = jolkaSolver.findStartingPositions()
        jolkaSolver.findDomainAvailableWords()
        jolkaSolver.findDomainCrossingWords(startingPositions)
        jolkaSolver.findMinimumDomain(startingPositions)
        #initial call with the original board and list of available words
        self.backtrackingFC(jolkaSolver,startingPositions, self.boardSetup,self.wordList)
    
    
    def backtrackingFC(self,jkSolver,startingPositions, pBoard,pWordsLeft):
        #we check for the minimum domain for filling a word
        i,j=jkSolver.findMinimumDomain(startingPositions)
        jkSolver = jkSolver.findDomainCrossingWords(startingPositions)
        #we have to check that the minimum found is a valid position
        #i.e. valid branch to continue
        if not i=='' and not j=='' and self.solutionFound == False:
            #we go over that min. domain
            domainHorizontalForChosenPosition = jkSolver.boardSetup[i][j][3]
            domainVerticalForChosenPosition = jkSolver.boardSetup[i][j][4]
            if domainHorizontalForChosenPosition is not None:
                for word in domainHorizontalForChosenPosition:
                    #copy by content, not by reference of the sudoku model
                    copyOfJolka = copy.deepcopy(jkSolver)
                    #we extract the first possibility from the remaining domain
                    #we insert it in the copy of the board
                    copyOfJolka = copyOfJolka.insertWordInPosition(word, i,j,"H")
                    #if it is not an unsolvable state we continue with the forward
                    #checking procedure
                    if copyOfJolka.isCrosswordSolvable(startingPositions):
                        self.backtrackingFC(copyOfJolka, startingPositions, copyOfJolka.boardSetup, copyOfJolka.wordList)
                    #we continue computing the domain for the temporal board
                    copyOfJolka = copyOfJolka.findDomainAvailableWords()
                    copyOfJolka = copyOfJolka.findDomainCrossingWords(startingPositions)
                    if copyOfJolka.isGameFinished():
                        print("")
                        print("")
                        print("the steps are done, solution(s) have been found")
                        copyOfJolka.printSimplifiedBoard()
                        self.solutionFound = True
                        break
            if domainVerticalForChosenPosition is not None:
                for word in domainVerticalForChosenPosition:
                    #copy by content, not by reference of the sudoku model
                    copyOfJolka=copy.deepcopy(jkSolver)
                    #we extract the first possibility from the remaining domain
                    #we insert it in the copy of the board
                    copyOfJolka = copyOfJolka.insertWordInPosition(word, i,j,"V")
                    #if it is not an unsolvable state we continue with the forward
                    #checking procedure
                    if copyOfJolka.isCrosswordSolvable(startingPositions):
                        self.backtrackingFC(copyOfJolka, startingPositions, copyOfJolka.boardSetup, copyOfJolka.wordList)
                    copyOfJolka = copyOfJolka.findDomainCrossingWords(startingPositions)
                    #we continue computing the domain for the temporal board
                    if copyOfJolka.isGameFinished():
                        print("")
                        print("")
                        print("the steps are done, solution(s) have been found")
                        copyOfJolka.printSimplifiedBoard()
                        self.solutionFound = True
                        break
   
        
start_time = time.time()
testJolka = fillInCSP("puzzle4","words4")
#print(testJolka.wordList)
testJolka.run()
print("--- %s seconds ---" % (time.time() - start_time))
if testJolka.solutionFound == False:
    print("No solution has been found for the current puzzle")
