import sys

outputFile='output'
refFile='t2'
#refFile='hashtags-train-maxmatch.txt'

def  minEditDist(target, source):
    ''' Computes the min edit distance from target to source. Figure 3.25 in the book. Assume that
    insertions, deletions and (actual) substitutions all cost 1 for this HW. Note the indexes are a
    little different from the text. There we are assuming the source and target indexing starts a 1.
    Here we are using 0-based indexing.'''
    
    n = len(target)
    m = len(source)

    distance = [[0 for i in range(m+1)] for j in range(n+1)]

    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + insertCost(target[i-1])

    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + deleteCost(source[j-1])

    for i in range(1,n+1):
        for j in range(1,m+1):
            distance[i][j] = min(distance[i-1][j]+insertCost(target[i-1]),
                                 distance[i][j-1]+insertCost(source[j-1]),
                                 distance[i-1][j-1]+substCost(source[j-1],target[i-1]))
    return distance[n][m]

def insertCost(ch):
    return 1
        
def deleteCost(ch):
    return 1       
    
def substCost(ch1,ch2):
    if ch1 == ch2:
        return 0
    return 1



def score():
    o = open(outputFile,'r')  
    r = open(refFile,'r')
    
    output = o.readlines()
    ref = r.readlines()
    
    print str(len(output)),
    print str(len(ref))
    scores=[]
    #print ("ref lines"+str(len(ref))),
    #print ("output lines"+str(len(output)))
    
    for i in range(len(output)):
        
        oTokens = output[i].strip().split()
        rTokens = ref[i].strip().split()
        
        #print (str(rTokens)),
        #print oTokens
        score = minEditDist(oTokens, rTokens)
        score = score*1.0/len(rTokens)
        scores.append(score)
        

    #print scores
    print "Error:"+ str( sum(scores)*1.0/len(scores) )
    o.close()
    r.close()
    
   
if __name__ == '__main__':                   
    #print 'Dist between them art I an and the martian --->' + str(minEditDist('them art i an','the martian'))
    #print 'Dist between them art I an and the martian --->' + str(minEditDist(['the', 'martian'],['them','art','i', 'an']))
    #print 'Dist between the dog and the cat --->' + str(minEditDist(['the', 'dog'],['the','cat']))
    #print 'Dist between The mart I an and the martian --->' + str(minEditDist('the mart i an','the martian'))
    #print 'Dist between Saturday and Sunday --->' + str(minEditDist('Saturday','Sunday'))
    if len(sys.argv) == 3:
        refFile = str(sys.argv[1])
        outputFile = str(sys.argv[2])
        score()
    else:
        print "Incorrect input arguments"    
        outputFile='output'
        refFile='t2'

        score()