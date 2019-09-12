#from sklearn_crfsuite import CRF

from util import *


class CRFModel(object):
    def __init__(self,
                 algorithm='lbfgs',
                 c1=0.1,
                 c2=0.1,
                 max_iterations=100,
                 all_possible_transitions=False
                 ):

        self.model = CRF(algorithm=algorithm,
                         c1=c1,
                         c2=c2,
                         max_iterations=max_iterations,
                         all_possible_transitions=all_possible_transitions)

    def train(self, sentences, tag_lists):
        features = [sent2features(s) for s in sentences]
        self.model.fit(features, tag_lists)

    def test(self, testWordLists, testTagLists, wordDict, tagDict):
        features = [sent2features(s) for s in testWordLists]
        tagPres = self.model.predict(features)

        goldEntity, preEntity, correctEntity = 0, 0, 0

        for index in range(len(tagPres)):
            sentence = str2int(testWordLists[index], wordDict) 
            tagPre = str2int(tagPres[index], tagDict)
            tag = str2int(testTagLists[index], tagDict)
            resultPre = extraEntity(sentence, tagPre, wordDict, tagDict)
            resultRel = extraEntity(sentence, tag, wordDict, tagDict)

            preEntity += len(resultPre)
            goldEntity += len(resultRel)
            correctEntity += len(match(resultPre, resultRel))
        
        print("------------------CRF-----------------------")
        print (goldEntity, preEntity, correctEntity)
        precise = 1.0 * correctEntity / preEntity
        recall = 1.0 * correctEntity / goldEntity
        F1 = (2 * precise * recall) / (precise + recall)
        print ('正确率:  %f' % precise)
        print ('召回率:  %f'% recall)
        print ('F1:  %f' % F1)

