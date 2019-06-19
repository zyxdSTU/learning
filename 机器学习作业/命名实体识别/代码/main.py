from util import *
from HMM import *
from hmmEM import *

wordDict, tagDict = acquireDict(['语料\\dev.char.bmes', '语料\\test.char.bmes', '语料\\train.char.bmes'])

tagDict = {'B-NAME': 0, 'M-NAME': 1, 'E-NAME': 2, 'O': 3, 'B-CONT': 4, 'M-CONT': 5, 'E-CONT': 6, 'B-EDU': 7,  
    'M-EDU': 8, 'E-EDU': 9, 'B-TITLE': 10, 'M-TITLE': 11, 'E-TITLE': 12, 'B-ORG': 13, 'M-ORG': 14, 'E-ORG': 15, 
        'B-RACE': 16, 'E-RACE': 17, 'B-PRO': 18, 'M-PRO': 19, 'E-PRO': 20, 'B-LOC': 21, 'M-LOC': 22, 'E-LOC': 23,
         'S-RACE': 24, 'S-NAME': 25, 'M-RACE': 26, 'S-ORG': 27, 'S-CONT':28, 'S-EDU':29,'S-TITLE':30, 'S-PRO':31,
         'S-LOC':32}

trainWordLists, trainTagLists = prepareData('语料\\train.char.bmes')
testWordLists, testTagLists = prepareData('语料\\test.char.bmes')

hmm = HMM(len(wordDict), len(tagDict))
hmm.trainSup(str2int(trainWordLists,wordDict), str2int(trainTagLists,tagDict))
hmm.test(str2int(testWordLists, wordDict), str2int(testTagLists, tagDict), wordDict, tagDict)

# hmm = HMM(len(wordDict), len(tagDict))

# discreteHMM = DiscreteHMM(len(tagDict),len(wordDict),100)
# discreteHMM.train_batch(trainWordLists)

# print (discreteHMM.emission_prob)
# print (discreteHMM.transmat_prob)
# print (discreteHMM.start_prob)

# hmm.emitProb = discreteHMM.emission_prob
# hmm.transitionProb = discreteHMM.transmat_prob
# hmm.initProb = discreteHMM.start_prob

# hmm.test(testWordLists, testTagLists, wordDict, tagDict)











       