from numpy import *
import numpy
import operator
from util import *

class HMM():
    '''
    wordDcitSize 词表长度
    tagDictSize 标签字典长度
    emitProb 观测概率矩阵
    transitionProb 转移概率矩阵
    initProb 初始概率向量
    '''
    def __init__(self, wordDictSize, tagDictSize):
        self.wordDictSize = wordDictSize
        self.tagDictSize = tagDictSize

        self.transitionProb = numpy.ones((tagDictSize, tagDictSize)) * (1.0 / tagDictSize)
        self.initProb = numpy.ones(tagDictSize) * (1.0 / tagDictSize)
        self.emitProb = numpy.ones((tagDictSize, wordDictSize)) * (1.0 / wordDictSize)

        # self.transitionProb = array([[0.5, 0.2, 0.3], [0.3, 0.5, 0.2], [0.2, 0.3, 0.5]])
        # self.initProb = array([0.2, 0.4, 0.4])
        # self.emitProb = array([[0.5, 0.5], [0.4, 0.6], [0.7, 0.3]])

    '''
    无监督学习
    iter为迭代次数
    '''
    def trianUnsup(self, trainWordLists, iter):
        for i in range(1, iter+1):
            print ("iter: ", i)
            '''
            E步
            '''
            bPostProb = []
            bAdjProb = numpy.zeros((self.tagDictSize, self.tagDictSize))
            bInitProb = numpy.zeros((self.tagDictSize))

            for wordList in trainWordLists:
                alpha = self.forwardAlg(wordList)
                beta = self.backwardAlg(wordList)

                #后验概率
                postProb = alpha * beta 
                for index in range(len(wordList)):
                    if numpy.sum(postProb[index]) != 0: postProb[index] = postProb[index] / numpy.sum(postProb[index])
                bPostProb.append(postProb)

                #联合概率
                adjProb = numpy.zeros((self.tagDictSize, self.tagDictSize))
                for j in range(len(wordList)):
                    if j == 0: continue
                    temp = numpy.outer(alpha[j-1], beta[j] * self.emitProb[:,wordList[j]]) * self.transitionProb
                    if numpy.sum(temp) != 0: adjProb += temp / numpy.sum(temp)

                #归一化
                if (numpy.sum(adjProb) != 0): adjProb = (adjProb.T / numpy.sum(postProb[:-1], axis=0)).T
                bAdjProb += adjProb

                #累加初始状态概率
                bInitProb += postProb[0]
            '''
            M步
            '''
            #更新初始概率
            self.initProb = bInitProb / numpy.sum(bInitProb)

            #更新转移概率
            self.transitionProb = array([bAdjProb[j] / numpy.sum(bAdjProb[j]) for j in range(self.tagDictSize)])

            #更新观测概率
            self.emitProb = numpy.zeros((self.tagDictSize, self.wordDictSize))
            for element, wordList in zip(bPostProb, trainWordLists):
                temp = numpy.zeros((self.tagDictSize, self.wordDictSize))
                for j, word in enumerate(wordList):
                    for k in range(self.tagDictSize):
                        temp[k, word] = temp[k, word] + element[j][k]
                temp = (temp.T / numpy.sum(element, axis=0)).T
                self.emitProb += temp

            for k in range(self.tagDictSize):
                if numpy.sum(self.emitProb[k]) != 0: self.emitProb[k] = self.emitProb[k] / numpy.sum(self.emitProb[k])

            self.emitProb[self.emitProb == 0] = 1e-10
            self.initProb[self.initProb == 0] = 1e-10
            self.transitionProb[self.transitionProb == 0] = 1e-10

            print (self.transitionProb)
            print (self.emitProb)
            print (self.initProb)

    '''
    监督学习, 极大似然估计
    '''
    def trainSup(self, trainWordLists, trainTagLists):
        self.transitionProb = numpy.zeros((self.tagDictSize, self.tagDictSize))
        self.initProb = numpy.zeros(self.tagDictSize) 
        self.emitProb = numpy.zeros((self.tagDictSize, self.wordDictSize))

        for i in range(len(trainWordLists)):
            for j in range(len(trainWordLists[i])):
                word, tag = trainWordLists[i][j], trainTagLists[i][j]
                self.initProb[tag] += 1
                self.emitProb[tag][word] += 1
                if j < len(trainWordLists[i])-1:
                    nextTag = trainTagLists[i][j+1]
                    self.transitionProb[tag][nextTag] += 1
        self.initProb = self.initProb / (self.initProb.sum())
        for index, value in enumerate(self.emitProb.sum(axis=1)):
            if value == 0: continue
            self.emitProb[index, :] = self.emitProb[index, :] / value

        for index, value in enumerate(self.transitionProb.sum(axis=1)):
            if value == 0: continue
            self.transitionProb[index, :] = self.transitionProb[index, :] / value

        self.initProb[self.initProb == 0] = 1e-10
        self.transitionProb[self.transitionProb == 0] = 1e-10
        self.emitProb[self.emitProb == 0] = 1e-10

    '''
    前向算法
    '''
    def forwardAlg(self, sentence):
        sentenceSize = len(sentence)
        alpha = numpy.zeros((sentenceSize, self.tagDictSize))
        alpha[0] = self.initProb * self.emitProb[:,int(sentence[0])]
        for index, word in enumerate(sentence):
            if index == 0: continue
            alpha[index] = numpy.dot(alpha[index-1], self.transitionProb) * self.emitProb[:,word]
        return alpha

    '''
    后向算法
    '''
    def backwardAlg(self, sentence):
        sentenceSize = len(sentence)
        beta = numpy.zeros((sentenceSize, self.tagDictSize))
        beta[sentenceSize-1] = numpy.ones(self.tagDictSize)
        for index in reversed(range(sentenceSize)):
            if index == sentenceSize-1: continue
            beta[index] = numpy.dot(beta[index+1] * self.emitProb[:,sentence[index+1]], self.transitionProb.T)
        return beta
 
    '''
    维特比算法
    '''
    def viterbiAlg(self, sentence):
        sentenceSize = len(sentence)
        score = numpy.zeros((sentenceSize, self.tagDictSize))
        path = numpy.zeros((sentenceSize, self.tagDictSize))

        score[0] = self.initProb + self.emitProb[:,sentence[0]]

        state = numpy.zeros(sentenceSize)

        for index, word in enumerate(sentence):
            if index == 0: continue
            temp = score[index-1] + self.transitionProb.T
            path[index] = numpy.argmax(temp, axis=1)
            score[index] = [element[int(path[index,i])] for i, element in enumerate(temp)] + self.emitProb[:,word]

        state[-1] = numpy.argmax(score[-1])
        
        for i in reversed(range(sentenceSize)):
            if i == sentenceSize -1: continue
            state[i] = path[i+1][int(state[i+1])]
        return state

    def test(self, testWordLists, testTagLists, wordDict, tagDict):
        self.transitionProb = numpy.log10(self.transitionProb)
        self.emitProb = numpy.log10(self.emitProb)
        self.initProb = numpy.log10(self.initProb)

        goldEntity, preEntity, correctEntity = 0, 0, 0
        for sentence, tag in zip(testWordLists, testTagLists):
            tagPre = self.viterbiAlg(sentence)
            resultPre = extraEntity(sentence, tagPre, wordDict, tagDict)
            resultRel = extraEntity(sentence, tag, wordDict, tagDict)
            #print (resultPre)
            preEntity += len(resultPre)
            goldEntity += len(resultRel)
            correctEntity += len(match(resultPre, resultRel))

        if correctEntity == 0: return
            
        print("------------------HMM-----------------------")
        print (goldEntity, preEntity, correctEntity)
        precise = 1.0 * correctEntity / preEntity
        recall = 1.0 * correctEntity / goldEntity
        F1 = (2 * precise * recall) / (precise + recall)
        print ('正确率:  %f' % precise)
        print ('召回率:  %f'% recall)
        print ('F1:  %f' % F1)



