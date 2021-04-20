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



    if positive_freq>negative_freq:
        max_sent_freq="positive"
    else:
        max_sent_freq="negative"

    #print(max_sent_freq)
    
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
 
    for j in range(0,len(trainWordsList)):
        contents = trainWordsList[j] #gets each tweet in the list of lists
        currentSent = senses[j] #gets current sent associated with each tweet

        # matchLine = "websiteLink"
        # for j in range(0,len(contents)):
        #     matchF=re.search(matchLine,contents[j])
        #     if matchF:
        #         locate = j


        for k in range(0,len(contents)): #traverses through the length of the tweet (which is the same as the length of the list because each word in a tweet is its own element)
            word = contents[k] #each word in each tweet
            #print(word)

            if word not in sentD:
                sentD[word]={}
                sentD[word]["positive"]=0
                sentD[word]["negative"]=0

                # if currentSent =="positive":
                #     sentD[word]["positive"]+=1
                # else:
                #     sentD[word]["negative"]+=1



            # if word not in sentD:
            #     sentD[word]={}
            #     if currentSent=="positive":
            #         sentD[word][currentSent]=0
            #     else:
            #         sentD[word]["negative"]=0

            #     # sentD[word]["positive"]=0
            #     # sentD[word]["negative"]=0

            # if word not in sentD:
            #     if currentSent=="positive":
            #         sentD[word]={}
            #         sentD[word]["positive"] =1
            #     else:
            #         sentD[word]={}
            #         sentD[word]["negative"]=1
            
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


    ##############################################################################################
    ########################################TESTING#######################
    contentsTest=cleanFile(contentsTest)
    #contentsTest = re.sub( r"\"", "",contentsTest)
    contentsTestSplit = contentsTest.splitlines()
    #print(contentsTestSplit)

    listInstance=[]
    for x in contentsTestSplit:
        instanceId = re.findall('<instance id="([^"]*)"', x)
        listInstance.append(instanceId)

    #print(listInstance)

    listInstanceFil=[]
    listInstanceFil = [x for x in listInstance if x != []]
    #print("instance list: ",listInstanceFil)

    for i,line in enumerate(contentsTestSplit):
        if line.startswith("<instance id="):
            contentsTestSplit[i]=""

    while("" in contentsTestSplit):
        contentsTestSplit.remove("")

    testWordsList = split_list(contentsTestSplit)

    pat = "website/(.*)"
    corp="</corpus>"
    for i,lst in enumerate(testWordsList):
        for index,word in enumerate(lst):
            match=re.search(pat,word)
            corpMatch = re.search(corp, word)

            if match:
                lst[index] = re.sub(r'website/(.*)', 'websiteLink', word)
            
            if corpMatch:
                lst[index]=re.sub(r'</corpus>',"",word)

            if "\"" in word:
                #print("word: ", word)
                lst[index]= word.replace('"', "")

    testWordsList = [x for x in testWordsList if x != ['']]

    #print("testing", testWordsList)

    with open(model, "a") as f:
        f.write("testing words list")
        print(testWordsList,file=f)


    miniLogDict={}
    count =0

    for index in range(0,len(testWordsList)): 
        contentsTest=testWordsList[index] #gets one tweet at a time
        #print(contentsTest)

        for p in range(0,len(contentsTest)): #traverses through one tweet at a time
            wordMatch = contentsTest[p] #grabs each word in tweet

            for keyL, valL in log_dict.items(): 
                if keyL ==wordMatch: #if the word from the tweet matches the key in log_dict
                    miniLogDict[keyL] = valL #store it into a mini dictionary with the key and value
            
        #print("mini log dict", miniLogDict)
        max_value = max(miniLogDict.values()) #get the highest max_value from the miniLogDict
        max_keys =[k for k, v in miniLogDict.items() if v == max_value] #gets the key associated with the max_value
        
        miniLogDict.clear()

        if len(max_keys)>1: #black 15 posi, 15 neg, if there are multiple words in one tweet that have the same log value, choose one randomly 
            max_keys =random.sample(max_keys,1)
        
       
        #print("Sent", sentD)
        for keyMax,valMax in sentD.items(): #{'does': {'positive': 1, 'negative': 3}
            for i in max_keys: #if key in sent d matches mini log dict key
                if keyMax ==i: #if word max_key --> one word key --> angela

                    max_num = max(valMax.values()) #pos 3, neg 4 --> 4 #gets the highest nested value
                    max_sent = [k for k, v in valMax.items() if v ==max_num] #--> neg --># gets the key associated with highest nested value

                    '''
                    the word black appears 15 times as positive and 15 as negatives, so it just selects a random one
                    to choose what the senitment of the tweet will be
                    '''

                    if len(max_sent)>1:
                        max_sent= random.sample(max_sent,1)

                    instanceNum = listInstanceFil[count]
                    #print(keyMax)
                    #print("max", max_num, "sent", max_sent)

                    #print(listInstanceFil[count])
                    finSent = ", ".join(max_sent)
                    finNum= ", ".join(instanceNum)
                   
                   
                    #accuracy 69.39655172413794
                    #print('<answer instance="'+finNum+'" sentiment="'+finSent+'"/>')

                    #Baseline Test = #68.96551724137932
                    print('<answer instance="'+finNum+'" sentiment="'+max_sent_freq+'"/>')
                    count+=1
                    
    


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