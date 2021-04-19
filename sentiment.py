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
 

    print(trainWordsList)



 

    



    ##########TESTING##############

    # listInstance=[]
    # for x in contentsTrainSplit:
    #     instanceId = re.findall('<instance id="([^"]*)"', x)
    #     listInstance.append(instanceId)

    # #print(listInstance)

    # listInstanceFil = [x for x in listInstance if x != []]
    #print(listInstanceFil)

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