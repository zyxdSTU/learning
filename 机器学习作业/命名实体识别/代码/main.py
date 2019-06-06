from util import *
from HMM import *

wordDict, tagDict = acquireDict(['语料\\dev.char.bmes', '语料\\test.char.bmes', '语料\\train.char.bmes'])

#print (len(wordDict))
tagDict = {'B-NAME': 0, 'M-NAME': 1, 'E-NAME': 2, 'O': 3, 'B-CONT': 4, 'M-CONT': 5, 'E-CONT': 6, 'B-EDU': 7,  
    'M-EDU': 8, 'E-EDU': 9, 'B-TITLE': 10, 'M-TITLE': 11, 'E-TITLE': 12, 'B-ORG': 13, 'M-ORG': 14, 'E-ORG': 15, 
        'B-RACE': 16, 'E-RACE': 17, 'B-PRO': 18, 'M-PRO': 19, 'E-PRO': 20, 'B-LOC': 21, 'M-LOC': 22, 'E-LOC': 23,
         'S-RACE': 24, 'S-NAME': 25, 'M-RACE': 26, 'S-ORG': 27, 'S-CONT':28, 'S-EDU':29,'S-TITLE':30, 'S-PRO':31,
         'S-LOC':32}

trainWordLists, trainTagLists = prepareData('语料\\train.char.bmes', wordDict, tagDict)

testWordLists, testTagLists = prepareData('语料\\test.char.bmes', wordDict, tagDict)

# wordDict = {'红':0, '白':1}

# tagDict = {'盒子1':0, '盒子2':1, '盒子3':2}

hmm = HMM(len(wordDict), len(tagDict))

#hmm.trianUnsup([[0,1,0]], 4)

hmm.trianUnsup(trainWordLists[:10], 4)
#hmm.test(testWordLists, testTagLists, wordDict, tagDict)








       