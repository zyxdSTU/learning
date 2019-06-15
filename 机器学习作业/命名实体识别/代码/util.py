from collections import OrderedDict
'''
准备数据
:filePath 文件路径
:wordlists 句子列表
:taglists 句子列表对应的标签列表
'''
def prepareData(filePath):
    f = open(filePath, 'r', encoding='utf-8', errors='ignore')
    wordlists, taglists = [], []
    wordlist, taglist = [], []
    for line in f.readlines():
        if line == '\n':
            wordlists.append(wordlist); taglists.append(taglist)
            wordlist, taglist = [], []
        else: 
            word, tag = line.strip('\n').split()
            wordlist.append(word); taglist.append(tag)
    if len(wordlist) != 0 or len(taglist) != 0:
        wordlists.append(wordlist); taglists.append(taglist)
    f.close()
    return wordlists, taglists

'''
数字标识转化为字符串
: origin是原来的数字标识(字典标识)
: dictionary 是对应的字典
'''
def int2str(origin, dictionary):
    result = []
    keys = list(dictionary.keys())
    if isinstance(origin[0], list):
        for i in range(len(origin)):
            result.append([])
            for j in range(len(origin[i])):
                result[i].append(keys[origin[i][j]])
    else:
        for i in range(len(origin)):
            result.append(keys[origin[i]])
    return result

'''
字符串转化为字典标识(数字)
: origin是原来的字符串
: dictionary 是对应的字典
'''
def str2int(origin, dictionary):
    result = []
    if isinstance(origin[0], list):
        for i in range(len(origin)):
            result.append([])
            for j in range(len(origin[i])):
                result[i].append(dictionary[origin[i][j]])
    else:
        for i in range(len(origin)):
            result.append(dictionary[origin[i]])
    return result

'''
获取词表、标签表
'''
def acquireDict(fileNameList):
    wordDict, tagDict = OrderedDict(), OrderedDict()
    for fileName in fileNameList:
        f = open(fileName, 'r', encoding='utf-8', errors='ignore')
        for line in f.readlines():
            if line == '\n': continue
            word, tag = line.strip('\n').split()

            if word not in wordDict:
                wordDict[word] = len(wordDict)

            if tag not in tagDict:
                tagDict[tag] = len(tagDict)
        f.close()
    return wordDict, tagDict

'''
根据标签, 提取实体
'''
def extraEntity(wordList, taglist, wordDict, tagDict):
    #print (wordList)
    #print (taglist)
    #print (list(''.join([list(wordDict.keys())[word] for word in wordList])))

    NAME = extraNameEntity(wordList, taglist, wordDict, tagDict)
    CONT = extraContEntity(wordList, taglist, wordDict, tagDict)
    EDU = extraEduEntity(wordList, taglist, wordDict, tagDict)
    TITLE = extraTitleEntity(wordList, taglist, wordDict, tagDict)
    ORG = extraOrgEntity(wordList, taglist, wordDict, tagDict)
    RACE = extraRaceEntity(wordList, taglist, wordDict, tagDict)
    PRO = extraProEntity(wordList, taglist, wordDict, tagDict)
    LOC = extraLocEntity(wordList, taglist, wordDict, tagDict)
    
    return NAME + CONT + EDU + TITLE + ORG + RACE + PRO + LOC

def extraNameEntity(wordList, tagList, wordDict, tagDict):
    NAME, name, flag = [], [], False
    for word, tag in zip(wordList, tagList):

        if tag == tagDict['S-NAME']:
            if flag == False: name.append(list(wordDict.keys())[word]); NAME.append(''.join(name)); name = []; continue

        if tag == tagDict['B-NAME']:
            if flag == False: name.append(list(wordDict.keys())[word]); flag = True; continue

        if tag == tagDict['M-NAME']:
            if flag == True: name.append(list(wordDict.keys())[word]); continue

        if tag == tagDict['E-NAME']:
            if flag == True: name.append(list(wordDict.keys())[word]); NAME.append(''.join(name)); flag == False; name = []; continue

        flag = False; name = []
    
    return [element + '-NAME' for element in NAME]

def extraContEntity(wordList, tagList, wordDict, tagDict):
    CONT, cont, flag = [], [], False
    for word, tag in zip(wordList, tagList):

        if tag == tagDict['S-CONT']:
            if flag == False: cont.append(list(wordDict.keys())[word]); CONT.append(''.join(cont)); cont = []; continue

        if tag == tagDict['B-CONT']:
            if flag == False: cont.append(list(wordDict.keys())[word]); flag = True; continue

        if tag == tagDict['M-CONT']:
            if flag == True: cont.append(list(wordDict.keys())[word]); continue

        if tag == tagDict['E-CONT']:
            if flag == True: cont.append(list(wordDict.keys())[word]); CONT.append(''.join(cont)); flag == False; cont = []; continue

        flag = False; cont = []

    return [element + '-CONT' for element in CONT]

def extraEduEntity(wordList, tagList, wordDict, tagDict):
    EDU, edu, flag = [], [], False
    for word, tag in zip(wordList, tagList):

        if tag == tagDict['S-EDU']:
            if flag == False: edu.append(list(wordDict.keys())[word]); EDU.append(''.join(edu)); edu = []; continue

        if tag == tagDict['B-EDU']:
            if flag == False: edu.append(list(wordDict.keys())[word]); flag = True; continue

        if tag == tagDict['M-EDU']:
            if flag == True: edu.append(list(wordDict.keys())[word]); continue

        if tag == tagDict['E-EDU']:
            if flag == True: edu.append(list(wordDict.keys())[word]); EDU.append(''.join(edu)); flag == False; edu = []; continue

        flag = False; edu = []

    return [element + '-EDU' for element in EDU]

def extraTitleEntity(wordList, tagList, wordDict, tagDict):
    TITLE, title, flag = [], [], False
    for word, tag in zip(wordList, tagList):

        if tag == tagDict['S-TITLE']:
            if flag == False: title.append(list(wordDict.keys())[word]); TITLE.append(''.join(title)); title = [];continue

        if tag == tagDict['B-TITLE']:
            if flag == False: title.append(list(wordDict.keys())[word]); flag = True; continue

        if tag == tagDict['M-TITLE']:
            if flag == True: title.append(list(wordDict.keys())[word]); continue

        if tag == tagDict['E-TITLE']:
            if flag == True: title.append(list(wordDict.keys())[word]); TITLE.append(''.join(title)); flag == False; title = []; continue

        flag = False; title = []

    return [element + '-TITLE' for element in TITLE]

def extraOrgEntity(wordList, tagList, wordDict, tagDict):
    ORG, org, flag = [], [], False
    for word, tag in zip(wordList, tagList):

        if tag == tagDict['S-ORG']:
            if flag == False: org.append(list(wordDict.keys())[word]); ORG.append(''.join(org)); org = []; continue

        if tag == tagDict['B-ORG']:
            if flag == False: org.append(list(wordDict.keys())[word]); flag = True; continue

        if tag == tagDict['M-ORG']:
            if flag == True: org.append(list(wordDict.keys())[word]); continue

        if tag == tagDict['E-ORG']:
            if flag == True: org.append(list(wordDict.keys())[word]); ORG.append(''.join(org)); flag == False; org = []; continue

        flag = False; org = []
    return [element + '-ORG' for element in ORG]

def extraRaceEntity(wordList, tagList, wordDict, tagDict):
    RACE, race, flag = [], [], False
    for word, tag in zip(wordList, tagList):

        if tag == tagDict['S-RACE']:
            if flag == False: race.append(list(wordDict.keys())[word]); RACE.append(''.join(race)); race = []; continue

        if tag == tagDict['B-RACE']:
            if flag == False: race.append(list(wordDict.keys())[word]); flag = True ; continue

        if tag == tagDict['M-RACE']:
            if flag == True: race.append(list(wordDict.keys())[word]); continue

        if tag == tagDict['E-RACE']:
            if flag == True: race.append(list(wordDict.keys())[word]); RACE.append(''.join(race)); flag == False; race = []

        flag = False; race = []
    return [element + '-RACE' for element in RACE]

def extraProEntity(wordList, tagList, wordDict, tagDict):
    PRO, pro, flag = [], [], False
    for word, tag in zip(wordList, tagList):

        if tag == tagDict['S-PRO']:
            if flag == False: pro.append(list(wordDict.keys())[word]); PRO.append(''.join(pro)); pro = []; continue

        if tag == tagDict['B-PRO']:
            if flag == False: pro.append(list(wordDict.keys())[word]); flag = True; continue

        if tag == tagDict['M-PRO']:
            if flag == True: pro.append(list(wordDict.keys())[word]); continue

        if tag == tagDict['E-PRO']:
            if flag == True: pro.append(list(wordDict.keys())[word]); PRO.append(''.join(pro)); flag == False; pro = []; continue
         
        flag = False; pro = []
    return [element + '-PRO' for element in PRO]

def extraLocEntity(wordList, tagList, wordDict, tagDict):
    LOC, loc, flag = [], [], False
    for word, tag in zip(wordList, tagList):

        if tag == tagDict['S-LOC']:
            if flag == False: loc.append(list(wordDict.keys())[word]); LOC.append(''.join(loc)); loc = []; continue

        if tag == tagDict['B-LOC']:
            if flag == False: loc.append(list(wordDict.keys())[word]); flag = True; continue

        if tag == tagDict['M-LOC']:
            if flag == True: loc.append(list(wordDict.keys())[word]); continue

        if tag == tagDict['E-LOC']:
            if flag == True: loc.append(list(wordDict.keys())[word]); LOC.append(''.join(loc)); flag == False; loc = []; continue
        
        flag = False; loc = []

    return [element + '-LOC' for element in LOC]
            

def match(listOne, listTwo):
    result = []
    for element in listOne:
        if element in listTwo:
            result.append(element)
    return result

def word2features(sent, i):
    """抽取单个字的特征"""
    word = sent[i]
    prev_word = '<s>' if i == 0 else sent[i-1]
    next_word = '</s>' if i == (len(sent)-1) else sent[i+1]
    # 使用的特征：
    # 前一个词，当前词，后一个词，
    # 前一个词+当前词， 当前词+后一个词
    features = {
        'w': word,
        'w-1': prev_word,
        'w+1': next_word,
        'w-1:w': prev_word+word,
        'w:w+1': word+next_word,
        'bias': 1
    }
    return features


def sent2features(sent):
    """抽取序列特征"""
    return [word2features(sent, i) for i in range(len(sent))]
        
