import pickle
import re
from heapq import *

wordMap = {}
wordDict = {}

wordListFileName = 'dictitr11'
dictToCheck = 'dictBIGWORDLIST'
inputWords = 'hashtags-test-2015.txt'
output_file = 'output'


numberPattern = r'^[0-9]+$'

def loadWords():
    fileObject = open(wordListFileName, 'r')  
    global wordMap
    wordMap = pickle.load(fileObject)
    fileObject.close()
    
    fileObject = open(dictToCheck,'r')  
    global wordDict
    wordDict = pickle.load(fileObject)
    fileObject.close()

def maxMatch(inputString):
    if len(inputString) == 0:
        return []
        
    pointer = len(inputString) - 1
    tokens = []
    
    while pointer >= 0:
        tokenizedString = inputString[:pointer + 1]
        if tokenizedString in wordMap:
            tokens.append(tokenizedString)
            remString = inputString[pointer + 1:]
            parsedRemString = maxMatch(remString)
            if len(parsedRemString) > 0:
                tokens = tokens + parsedRemString
            return tokens    
        pointer = pointer - 1        
    tokens.append(inputString[0])
    parsedRemString = maxMatch(inputString[1:])
    tokens = tokens + parsedRemString
    
    return tokens 
  
parsedDict = {}

def modifiedMaxMatch(inputString):

    if len(inputString) == 0:
        return ((0, 0, 0), [])
    if inputString in parsedDict:
        return parsedDict[inputString]
    
    # print "parsing "+inputString    
    
    heap = []    
    
    pointer = len(inputString) - 1
    
    
    while pointer >= 0:
        tokenizedString = inputString[:pointer + 1]
        if tokenizedString in wordMap:
            tokens = []
            tokens.append(tokenizedString)
            parsedRemString = modifiedMaxMatch(inputString[pointer + 1:])
            updateHeap(heap, parsedRemString, tokens, 0)
        pointer = pointer - 1        
    
    tokens = []    
    tokens.append(inputString[0])
    parsedRemString = modifiedMaxMatch(inputString[1:])
    updateHeap(heap, parsedRemString, tokens, 1)

    parsedDict[inputString] = heappop(heap)
    return parsedDict[inputString]

def updateHeap(h, item, tokens, increment):

    (skips, parsedRemString) = item
    parseOutput = tokens + parsedRemString;
    #scoreTuple = (skips[0] + increment, len(parseOutput), scoreBasedOnDict(parseOutput))
    # scoreTuple = (skips[0]+increment,len(parseOutput),scoreBasedOnLength(parseOutput))
    # scoreTuple = (skips[0]+increment,len(parseOutput),1)
    scoreTuple = (skips[0] + increment, len(parseOutput), scoreBasedOnDict(parseOutput))
    heapItem = (scoreTuple, parseOutput)
    heappush(h, heapItem)

def scoreBasedOnDict(lst):
    i = 0
    for j in lst:
        if j in wordDict:
            i = i + 1
    if i == 0:
        i = i + 1        
    return len(lst)*1.0/i 
    pass            

def printQueue(q):
    while not q.empty():
        print (q.get()),
    print ''
                    
def segmentWords():
    fileObject = open(inputWords, 'r') 
    segmentedWordList = [] 
    for hashtag in fileObject:
        # tokens=maxMatch(hashtag.strip().lower())
        inputString = hashtag.strip().lower()
        prelimTokens = tokeninze(r'[0-9]+', inputString)
        if len(prelimTokens) == 1:
            (skip, tokens) = modifiedMaxMatch(inputString)
            segmentedWordList.append(tokens)
        else:
            p1=0
            tTokens=[]
            for t in prelimTokens:
                if re.search(numberPattern, t):
                    tTokens.append(t)
                else:
                    (skip, tokens) = modifiedMaxMatch(t)
                    p1=skip[0]+p1
                    for t in tokens:
                        tTokens.append(t)
                    
            item1=((p1,len(tTokens),1),tTokens)        
            item2 = modifiedMaxMatch(inputString)
            heap = []    
            updateHeap(heap, item1, [], 0)
            updateHeap(heap, item2, [], 0)
            
            segmentedWordList.append(heappop(heap)[1])
            
            
                        
                    
                
                
    fileObject.close()
    writeWords(segmentedWordList)    
    print 'done'

def tokeninze(pattern, text):
    start = 0
    tokens = []
    for match in re.finditer(pattern, text):
        s = match.start()
        e = match.end()
        if start != s:        
            tokens.append(text[start:s])
        tokens.append(text[s:e])
        start = e
    if start != len(text):    
        tokens.append(text[start:])    
    return tokens
    
def writeWords(segmentedWordList):
    my_file = open(output_file, "w")
    
    for i in segmentedWordList:
        str1 = ''
        for j in i:
            str1 = str1 + j + " "
                
        str1 = str1.strip()
        my_file.write(str1 + "\n")
    my_file.close() 
       
if __name__ == '__main__':
    loadWords()    
    segmentWords()

