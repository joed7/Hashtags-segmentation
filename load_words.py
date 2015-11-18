import pickle

a={}
words = "mlist11"
file_Name = "dictitr11"

def createPickle():
    # open the file for writing
    wordsObj = open(words,'r')

    for i in wordsObj:
        a[i.strip().lower()]=1 

    # open the file for writing
    fileObject = open(file_Name,'wb') 

    # this writes the object a to the
    # file named 'testfile'
    pickle.dump(a,fileObject)   
    # here we close the fileObject
    fileObject.close()

def loadPickle():
    # we open the file for reading
    fileObject = open(file_Name,'r')  
    # load the object from the file into var b
    b = pickle.load(fileObject)  
    print len(b)

createPickle()
loadPickle()

