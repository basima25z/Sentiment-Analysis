'''
#Basima Zafar
#CMSC 416: Natural Language Processing
#Progamming Assignment 5: Sentiment
#The purpose of this program is to analyze the sentiment of Tweets and catagorize each Tweet as either positve or negative
#In order to do this, you have to train your sentiment analyzer on your training data and utilize what it has learned on the testing data
#The training file has Tweets as well as the sentiment that it is
#The testing file has Tweets and when we run it through the sentiment program, our goal to accurately catagorize it as either
# a positive or negative based off the log likely hood 
#The output utilies STDOUT, so in the command line, following the two files, use '>' along with the filename.txt that you would like to output to
#To run this program in the terminal the commands are: python3 sentiment.py sentiment-train.txt sentiment-test.txt my-model.txt > my-sentiment-answers.txt
#It is not necceasry to add the 3.8 after python unless you're IDE defaults to the python 2.7 interpretor 
'''
import os
import sys
import re
import csv
import itertools
from collections import Counter
import string
import math
import random

'''
################################################################
# Fucntion: Main
# Parameter: command line arguments
# The purpose of the main method is to read three files from the command line
# The program outputs to STDOUT, hence when the '>' is typed in following a filename.txt anything that 
# prints in the program will output directy to that file (within the same directory)
# After the files are read, the words unnecessary in the file are removed with a series of regex statements (words like corupus, lexlt, etc.) located in the cleanFile method
# There is also a regex statement to remove unncessary punctuation, such as an exclamation point, we have to remove so that it is not included as word (this happens if there is a space between the word and punctuation)
###############################################################
'''

def main(argv):
    trainFile = os.path.basename(sys.argv[1])
    testingFile = os.path.basename(sys.argv[2])
    model = os.path.basename(sys.argv[3])

    openTrainFile = open(trainFile, "r")
    contentsTrain = openTrainFile.read().lower()


    openTestFile = open(testingFile, "r")
    contentsTest = openTestFile.read().lower()



    ############### TRAINING#############
    contentsTrain=cleanFile(contentsTrain) #calls cleanFile method, this will return the file without words like corpus, lexlt , and etc.
    contentsTrainSplit=contentsTrain.splitlines() #Splits the training file to return a list of lines in a string, each line is its own index


    pattern='sentiment="([^"]*)"' #pattern to search for in the loop below
    senses=[] #this will be used to keep track of which sentiment goes with each tweet
    positive_freq=0
    negative_freq=0

    for i in contentsTrainSplit: #traverse through the contestTrainSplit
        match = re.search(pattern, i) #utilizing regex search for the word sentiment in each line
        if match: #if there is a match found
            sense=match.group(1) #captures group of words that match the regex pattern --> this would either be positive or negative
            senses.append(sense) #appends the match to the senses list

            if sense=='positive': #if the sense is positive
                positive_freq+=1 #increases the positive frequency
            else: #otherwise it increases the negative frequency
                negative_freq+=1
    
    


    #Baseline Implementation
    #The baseline implementation is based off whatever occured most frequently in the training file
    #This finds out which occured the most by comparing the frequencies 
    if positive_freq>negative_freq: #if the positive frequency is greater than the negative, assigned the max_sent_freq variable to positive
        max_sent_freq="positive"
    else: #else the max_sent_freq variable is set to negative
        max_sent_freq="negative"

    

    finTrain =[] #initilazing list to append to 

    for i in contentsTrainSplit[2::3]: #list slicing gets rid of the instance id and sense id, now we just have the text we need
        finTrain.append(i)

    #There were some quotations within the Tweets, so this loops through the list and if the word contains a quotation mark, it replaces it
    newFinTrain =[]
    for word in finTrain:
        newFinTrain.append(word.replace('\"',''))
    
    #calls the split_list method that seperates each tweet into an list of arrays
    trainWordsList = split_list(newFinTrain)

    #Each link is unique in the training data, so I utilized regex to replace each link with the word websiteLink
    #I took this route because otherwise, we would have unneccessary values in our log and sent dictionary because our
    # testing set would never find a match because all of the links across both sets are unique
    #If this wasn't done, we would be ignoring the links all together in our sentiment analysis, this way we can group the links
    # into one catagory and have a positive and a negative count

    pat = "website/(.*)" #pattern to search for
    for i,lst in enumerate(trainWordsList): #traversing through the list of array
        for index,word in enumerate(lst): #searching through each word in the list (of arrays)
            match=re.search(pat,word) #compare pattern to each word in the list

            if match: #if there is a match found
                lst[index] = re.sub(r'website/(.*)', 'websiteLink', word) #replace the link with the word "websiteLink" in the same index that the pattern matched
 

    #creation of dictionary sentD--> this will be utilized to create a nested dictionary in the if statements below
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
            word = contents[k] #captures each word in each tweet
           

            if word not in sentD: #if the word is not in the sentD dictionary, it initializes the dictionaries and add the word, but both values remain 0
                sentD[word]={}
                sentD[word]["positive"]=0
                sentD[word]["negative"]=0
            
            if word in sentD: #after the first if statement, the word is in the sentD dictionary, so now this will increase the value depending on whether the current sent is positive or negative
                if currentSent=="positive":
                    sentD[word]["positive"]+=1
                else:
                    sentD[word]["negative"]+=1
        

    with open(argv[3], "w") as f:
        f.write("Sentiment Dict")
        print(sentD,file=f)
    
    #The two dictionaries below are used to classify the numerator and denominator for the log likelyhood (prior to dividing them and applying log)
    #For each word with the sentiment "positive", it finds the number of times the word occured with "positive" and then divides by the total positive count
    
    #Number of time positive occurred with word divided by the total positive count 
    pos_dict = {word:sentD[word]['positive']/positive_freq for word in sentD.keys()}

    #For each word with the sentiment "negative", it finds the number of times the word occured with "negative" and then divides by the total negative count
    neg_dict = {word:sentD[word]['negative']/negative_freq for word in sentD.keys()}

    #When you calculate log, you can get a negative infinity if your numerator is a 0 and a positive infinity if youur denominator is 0
    #The below for loops traverse through the positive dict and the negative dict and checks to see if the value is 0.0 if it is, replaces it with a 0.1

    for keyP,valueP in pos_dict.items():
        if (valueP==0.0):
            pos_dict[keyP]=0.1

    for keyN,valueN in neg_dict.items():
        if (valueN==0.0):
            neg_dict[keyN]=0.1


    #This divides the value of the positve dict by the negative dict and stores it in the div dict, the key would be the word, and the value would the division value
    div={x:float(pos_dict[x])/neg_dict[x] for x in neg_dict}


    log_dict ={} #initalizes the log_dict to add to later
    for keyL,valL in div.items(): #for each key and value in the div dict
        temp = math.log10(valL) #find the log value of each value
        log_dict[keyL]=abs(temp) #take the absolute value of the log value and store it with the word in the log_dict

    with open(model, "a") as f:
        f.write("Log Dict")
        print(log_dict,file=f)


    ##############################################################################################
    ########################################TESTING#######################
    contentsTest=cleanFile(contentsTest) #calls cleanFile method to remove unneccessary words and punctuation
    #contentsTest = re.sub( r"\"", "",contentsTest)
    contentsTestSplit = contentsTest.splitlines() #Splits the testing file to return a list of lines in a string, each line is its own index


    #in order to print the correct output, we have to keep track of the instance id number
    listInstance=[] 
    for x in contentsTestSplit: #traverses through each line in the contentsTestSplit
        instanceId = re.findall('<instance id="([^"]*)"', x) #if the line contains the instance id
        listInstance.append(instanceId) #append the instance id to the listInstance list


    listInstanceFil=[]
    listInstanceFil = [x for x in listInstance if x != []] #if the listInstance is not empty, append it to a new list called listInstanceFil
    

    #After appending all the instance id, we need to remove instance id from the list prior to analyzing sentiments
    for i,line in enumerate(contentsTestSplit): #traverses through the list
        if line.startswith("<instance id="): #if the line starts with "<instance id="
            contentsTestSplit[i]="" #replaces the line where "<instance id=" occurs
 
    while("" in contentsTestSplit): #while there are empty indicies in contentsTestSplit
        contentsTestSplit.remove("") #removes the empty indicies 

    #calls the split_list method that seperates each tweet into an list of arrays
    testWordsList = split_list(contentsTestSplit)


    #Utilizing regex to clean up the testing file
    #Searches for the word website and replaces it with websiteLink
    #Searches for the word coprus and replaces it with an empty value
    #Search each word for a quation mark, and replaces it with an empty value
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
                lst[index]= word.replace('"', "")

    #If the index is not empty, then appends it to a new list called testWordsList
    #This has to be done to ensure that we only have indicies with actual tweets in them and not empty spaces
    testWordsList = [x for x in testWordsList if x != ['']]


    # with open(model, "a") as f:
    #     f.write("Testing Words List")
    #     print(testWordsList,file=f)


    miniLogDict={} #this miniLogDict will hold any matches that are found between the testing set and the training set
    count =0

    with open(model, "a") as f:
        for index in range(0,len(testWordsList)):  #traverse through testWordsList which contains a list of lists 
            contentsTest=testWordsList[index] #gets one tweet at a time (each tweet is its own sublist in the list testWordsList)

            for p in range(0,len(contentsTest)): #traverses through the length of the tweet
                wordMatch = contentsTest[p] #grabs each word in tweet

                for keyL, valL in log_dict.items(): #traverses through log_dict to see if the word from the tweet matches the key in log_dict
                    if keyL ==wordMatch: #if the word from the tweet matches the key in log_dict
                        miniLogDict[keyL] = valL #store it into a mini dictionary with the key and value

                
            max_value = max(miniLogDict.values()) #get the highest max_value from the miniLogDict
            max_keys =[k for k, v in miniLogDict.items() if v == max_value] #gets the key associated with the max_value
            
            miniLogDict.clear() #clears the miniLogDict, this is neccessary otherwise it will hold more than one Tweets value at a time

            if len(max_keys)>1: #if there are multiple words in one tweet that have the same log value, choose one randomly 
                max_keys =random.sample(max_keys,1)
            
            #traverses through the sentD dictionary
            #{'does': {'positive': 1, 'negative': 3} --> this is an example of how sentD looks
            #keyMax = "does", valMax = {'positive': 1, 'negative': 3} 
            
            for keyMax,valMax in sentD.items():  #traverses through the sentD
                for i in max_keys: #traverses through the values in max_key (which will always only be one value)
                    if keyMax ==i: #if the key in sentD (which is the word) is equal to the word in max_key

                        max_num = max(valMax.values()) #gets the highest nested value --> in the does example, this would get the number 3
                        max_sent = [k for k, v in valMax.items() if v ==max_num] # gets the key associated with highest nested value --> either gets positive or negative

                        
                        #the word black appears 15 times as positive and 15 as negatives, so below it just selects a random one
                        # to choose what the senitment of the tweet will be if the length of max_sent is greater than one
                        
                        if len(max_sent)>1:
                            max_sent= random.sample(max_sent,1)

                        instanceNum = listInstanceFil[count] #traversing through listInstanceFil
   
                        #print(listInstanceFil[count])
                        finSent = ", ".join(max_sent) #similar to casting, it makes the list into string
                        finNum= ", ".join(instanceNum)

                        f.write("Instance ID: " + finNum + "\n")
                        f.write("Word Matched: "+ keyMax + "\n")
                        f.write("Max Sent with Word Matched: " + finSent + "\n")
                        f.write(""+"\n")

                    
                    
                    
                        #Accuracy = 69.39655172413794
                        print('<answer instance="'+finNum+'" sentiment="'+finSent+'"/>')
                        

                        #Baseline Accuracy = #68.96551724137932
                        #print('<answer instance="'+finNum+'" sentiment="'+max_sent_freq+'"/>')

                        count+=1
            
                    
    


def cleanFile(fileName):
     fileName=re.sub(r'<[/]?corpus(.*)>\s|<[/]?lexelt(.*)>\s|<[/]?context>\s|</instance>\s',"",fileName)
     fileName=re.sub(r'[!#?,():.;-]'," ",fileName) 

     return fileName

def split_list(finTrain):
    return[item.split() for item in finTrain] #splits item sent in
    


if __name__ == "__main__":
    main(sys.argv)