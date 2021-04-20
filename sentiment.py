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
    time =0
    count =0

    for index in range(0,len(testWordsList)): 
        contentsTest=testWordsList[index] #gets one tweet at a time
        #print(contentsTest)

        for p in range(0,len(contentsTest)): #traverses through one tweet at a time
            wordMatch = contentsTest[p] #grabs each word in tweet

            for keyL, valL in log_dict.items(): 
                if keyL ==wordMatch: #if the word from the tweet matches the key in log_dict
                    miniLogDict[keyL] = valL #store it into a mini dictionary with the key and value
            #print(p)
            #print(miniLogDict)

        max_value = max(miniLogDict.values()) #get the highest max_value from the miniLogDict
        max_keys =[k for k, v in miniLogDict.items() if v == max_value] #gets the key associated with the max_value
        
        miniLogDict.clear()

        if len(max_keys)>1:
            max_keys =random.sample(max_keys,1)
        
        #print(max_keys)

        #print("listi", listInstanceFil)

        #TODO: think about if positive and negative is both equal to 1?
        for keyMax,valMax in sentD.items():
            for i in max_keys:
                if keyMax ==i: #if word max_key --> one word key --> angela
                    max_num = max(valMax.values())
                    max_sent = [k for k, v in valMax.items() if v ==max_num]

                    '''
                    the word black appears 15 times as positive and 15 as negatives, so it just selects a random one
                    to choose what the senitment of the tweet will be
                    '''

                    if len(max_sent)>1:
                        max_sent= random.sample(max_sent,1)

                    instanceNum = listInstanceFil[count]
                    # print(keyMax)
                    # print("max", max_num, "sent", max_sent)

                    #print(listInstanceFil[count])
                    finSent = ", ".join(max_sent)
                    finNum= ", ".join(instanceNum)
                   
                    #print(finNum, finSent)
                    #print(", ".join(instanceNum))

                    print('<answer instance="'+finNum+'" sentiment="'+finSent+'"/>')

                    #print('<answer instance="',instanceNum[-2:2],'" sentiment="',max_sent,'"/>')
                    count+=1
                    















                    # for k2,v2 in valMax.items():
                    #     max_num = max(valMax.values())
                    #     print("v2", v2)
                        


                    #print(keyMax,i)


                    # max_sentList =[]
                    # for k2,v2 in valMax.items(): #positive 3 --> k2,v2
                    #     # max_num = max(valMax.values())
                    #     # max_sent = [k for k, v in valMax.items() if v ==max_num]
                    #     # sentFin = str(max_sent[0])
                    #     # #print(k2,v2)
                    #     # print(max_num,sentFin)

                    #     itemMaxValue = max(valMax.items(), key=lambda x : x[1])
                    #     print(itemMaxValue)

                        #if v2=max_num:

                        # max_sent = [k for k, v in valMax.items() if v ==max_num]
                        # print(str(max_sent))

                        #max_value_keys = [valMax[x] for x in valMax.keys if valMax[x] == max(valMax.values())]

                        #print(max_num, max_value_keys)

                        # max_num, max_sent = max(((v,k) for inner_d in valMax.values() for k,v in inner_d.items()))
                        # print(max_num,max_sent)



                        # for i in max_sent[::-1]: #list slicing gets rid of the instance id and sense id, now we just have the text we need
                        #     max_sentList.append(max_sent)
                        # print(max_sentList)
                        #max_sentList.append(max_sent[0][0])
                        # print("length max sent: ",len(max_sent))



                        # #listInstance = [x for x in listInstance if x != []]
                        # finNum = str(listInstance[count])
                        # #print(finNum)
                        # print(finNum,max_sent)
                        # count = count+1
                        
                        #num = str(listInstanceFil[time])
                        #print('<answer instance="',num,'" sentiment="',max_sent,'"/>')
                        #time+=1

                        # for m in listInstanceFil:
                        #     okay = m
                        #     print(okay)
                        #     #print('<answer instance="'+okay+'" sentiment="'+max_sent+'"/>')
                        #     print(m)


                        #print(listInstanceFil[ok])
                        #finAns = str(listInstanceFil[count])#[2:-2]
                        #finSent =str(max_sent)[2:-2]
                        #print("max sent",max_sent)
                        #print("MAX: ",max_num, "sent: ", max_sent)
                        #print("match: ", i, k2,v2)

                        #print('<answer instance="',finAns,'" sentiment="',finSent,'"/>')
                        #print('<answer instance="'+finAns+'" sentiment="'+finSent+'"/>')
                    #print(max_sentList)
    
                

        

        #print(listInstanceFil[count])
        # for keyMax, valMax in sentD.items():
        #     for i in max_keys:
        #         if keyMax == i:
        #             max_val =0

        #             for k2,v2 in valMax.items():
        #                 print(listInstanceFil[count])
                        # if v2>max_val: #if the value in nested dicts is greater than max_val 
                        #     max_val =v2 #assigns the highest value in the nested dict to max_val
                        #     finalSense = k2 #assigns the sense (product or phone) that correlates to the highest value to finalSense variable 
                        #     finAns = str(listInstanceFil[count])#[2:-2] #uses list slicing get rid of [''] and str(list) to capture the line number in the dict
                        #     #Print to STDOUT
                        #     print('<answer instance="'+finAns+'" senseid="'+finalSense+'"/>')
                        #     count = count+1 #uses as an iterator to iterate through listInstanceFil

        # print(count)
        # count+=1
        #print("MAX: ",max_value,"MAX KEY: ",max_keys)
        
            
            #print(wordMatch)
            # keyWordMatch = p



            # if (locateTest-1) >= 0:
            # left_word_test = "L-1: " + contentsTest[locateTest-1] 
            # #If key in log_dict (key = word (ex: telephonek_1)) matches the left_word that was captured
            # #It adds the word and log value as the key and value into the miniLogDict
            # #The purpose of the miniLogDict is to hold the word and the log if a match if found between the log_dict and the word captured from the testing file
            # #The same process goes on for each rule in the next few if statements

            # for keyL, valL in log_dict.items():
            #     if keyL ==left_word_test: 
            #         miniLogDict[keyL] = valL




    

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