#Basima Zafar
#PA 5
import os
import sys
import re
import csv
import itertools
from collections import Counter
import string
import math
import random

def main(argv):
    trainFile = os.path.basename(sys.argv[1])
    testingFile = os.path.basename(sys.argv[2])
    model = os.path.basename(sys.argv[3])

    openTrainFile = open(trainFile, "r")
    contentsTrain = openTrainFile.read().lower()


    openTestFile = open(testingFile, "r")
    contentsTest = openTestFile.read().lower()



    ############### TRAINING#############
    contentsTrain=cleanFile(contentsTrain)
    #print(contentsTrain)
    contentsTrainSplit=contentsTrain.splitlines() #\n occurs when splitting
    #print(contentsTrainSplit)

    pattern='sentiment="([^"]*)"'
    senses=[]
    positive_freq=0
    negative_freq=0

    for i in contentsTrainSplit:
        match = re.search(pattern, i)
        if match:
            sense=match.group(1)
            senses.append(sense)

            if sense=='positive':
                positive_freq+=1
            else:
                negative_freq+=1

    
    #print(contentsTrainSplit) #for some reason if you print this here you get isn\ 't, but if you print this above matching its normal isn't

    finTrain =[]

    for i in contentsTrainSplit[2::3]: #list slicing gets rid of the instance id and sense id, now we just have the text we need
        finTrain.append(i)

    #print(finTrain) #gets context but has isn\'t

    newFinTrain =[]
    for word in finTrain:
        newFinTrain.append(word.replace('\"',''))
    
    #print(newFinTrain)

    trainWordsList = split_list(newFinTrain)

    #print(trainWordsList)

    pat = "website/(.*)"
    for i,lst in enumerate(trainWordsList):
        for index,word in enumerate(lst):
            match=re.search(pat,word)

            if match:
                lst[index] = re.sub(r'website/(.*)', 'websiteLink', word)
 
    #print(trainWordsList)

    # for i2,list2 in enumerate(trainWordsList):
    #     print(trainWordsList[i2])

    sentD={}
    count =0
    for j in range(0,len(trainWordsList)):
        contents = trainWordsList[j] #gets each tweet in the list of lists
        currentSent = senses[j] #gets current sent associated with each tweet


        # print(count, contents)
        # print(currentSent)
        # print(len(contents))
        count+=1


        for k in range(0,len(contents)): #traverses through the length of the tweet (which is the same as the length of the list because each word in a tweet is its own element)
            word = contents[k] #each word in each tweet
            #print(word)

            if word not in sentD:
                sentD[word]={}
                sentD[word]["positive"]=0
                sentD[word]["negative"]=0
            
            if word in sentD:
                if currentSent=="positive":
                    sentD[word]["positive"]+=1
                else:
                    sentD[word]["negative"]+=1
        
    #print("dicts", sentD)

    with open(argv[3], "w") as f:
        f.write("Sentiment Dict")
        print(sentD,file=f)
    
    #print("freq p", positive_freq)
    #print("freq n",negative_freq)


    pos_dict = {word:sentD[word]['positive']/positive_freq for word in sentD.keys()}
    neg_dict = {word:sentD[word]['negative']/negative_freq for word in sentD.keys()}

    #print("pos dict", pos_dict)
    #print("neg dict", neg_dict)

    for keyP,valueP in pos_dict.items():
        if (valueP==0.0):
            pos_dict[keyP]=0.1

    for keyN,valueN in neg_dict.items():
        if (valueN==0.0):
            neg_dict[keyN]=0.1


    div={x:float(pos_dict[x])/neg_dict[x] for x in neg_dict}

    #log_dict={b:abs(math.log(b)) for b in div}

    log_dict ={}
    for keyL,valL in div.items():
        temp = math.log10(valL)
        log_dict[keyL]=abs(temp)

    with open(model, "a") as f:
        f.write("Log Dict")
        print(log_dict,file=f)

    #print("division", div)

    #print("log dict", log_dict)


    ####################################################################

    #######TESTING#######################
    contentsTest=cleanFile(contentsTest)
    #contentsTest = re.sub( r"\"", "",contentsTest)
    contentsTestSplit = contentsTest.splitlines()
    #print(contentsTestSplit)

    listInstance=[]
    for x in contentsTestSplit:
        instanceId = re.findall('<instance id="([^"]*)"', x)
        listInstance.append(instanceId)

    #print(listInstance)

    listInstanceFil = [x for x in listInstance if x != []]
    print("instance list: ",listInstanceFil)

    for i,line in enumerate(contentsTestSplit):
        if line.startswith("<instance id="):
            contentsTestSplit[i]=""

    while("" in contentsTestSplit):
        contentsTestSplit.remove("")

    testWordsList = split_list(contentsTestSplit)

    pat = "website/(.*)"
    for i,lst in enumerate(testWordsList):
        for index,word in enumerate(lst):
            match=re.search(pat,word)

            if match:
                lst[index] = re.sub(r'website/(.*)', 'websiteLink', word)

    print("testing", testWordsList)

    
    

    # miniLogDict ={}

    # count=0
    # for index in range(0,len(testWordsList)): 
    #     contentsTest=testWordsList[index]

    #print(contentsTestSplit)

    ######################################
    




def cleanFile(fileName):
     fileName=re.sub(r'<[/]?corpus(.*)>\s|<[/]?lexelt(.*)>\s|<[/]?context>\s|</instance>\s',"",fileName)
     '''
        <instance id="620821002390339585">
        <answer instance="620821002390339585" sentiment="negative"/>
        does @macleansmag still believe that ms. angela merkel is the "real leader of the free world"?  http://t.co/isqfoicod0 (greeks may disagree
     '''
     #looks like this^ need to get instance id num and sentiment of each thing
     #fileName=re.sub(r'[!#?,().;:-]'," ",fileName)
     #fileName=re.sub(r'http[s]?://t.co(.*?)',"website", fileName)#[^\s]+
     fileName=re.sub(r'\bhttp[s]?://t.co(.*?)\b',"website", fileName)#[^\s]+
     fileName=re.sub(r'[!#?,():.;-]'," ",fileName) #need to add :, but left out bc of website

     return fileName

def split_list(finTrain):
    return[item.split() for item in finTrain] #splits item sent in
    


if __name__ == "__main__":
    #print('---------------------------------------------------------------------------------------------')
    #print('Basima Zafar')
    main(sys.argv)