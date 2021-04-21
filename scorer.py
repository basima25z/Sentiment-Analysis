'''
- Basima Zafar
- CMSC: 416 - Natural Language Processing
- April 7th, 2021
- Programming Assignment 5
- This is a utility program that compares the output from sentiment.py to the key provided to us
- The purpose of this program is to see how accuracte sentiment.py is at classifying the sentimenet of the Tweet as either positive or negative 
- We can see accuracy and precision with the confusion matrix and the accuracy score
- The input through the command line requires two files: my-sentiment-answers.txt and sentiment-test-key.txt
- The first file is the result of sentiment.py (which was printed to STDOUT)
- The output file will be utilizing STDOUT, so the > symbol along with a file name is needed in the command line,
so that the output knows where to be printed - along with the confusion matrix being output to STDOUT, a more easily readibly confusion
will pop up when the command is ran 
- To run this program, type in the command line:python3 scorer.py my-sentiment-answers.txt sentiment-test-key.txt > report.txt
- It is not necceasry to add the 3.8 after python unless you're IDE defaults to the python 2.7 interpretor
- Note: in order to close out of this program and to write to STDOUT, you must exit the pop up python box which displays the confusion matrix
'''
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import os
import sys
import re
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

#python3 scorer.py my-sentiment-answers.txt sentiment-test-key.txt > report.txt
'''
########################################################
# Function: Main
# Parameters: argv
# The main method takes in two files, the first being the outputfile from sentiment.py and the second being the sentiment-test-key.txt provided
# It opens up the two files and splits the two files and uses regex to just obtain the sentiment from both the test and the key provided
#########################################################
'''

def main(argv):
    testFile = os.path.basename(sys.argv[1])
    keyFile = os.path.basename(sys.argv[2])

    openTestFile = open(testFile, "r")
    contentsTest = openTestFile.read().lower()

    openKeyFile = open(keyFile, "r")
    contentsKey = openKeyFile.read().lower()

    contentsTestWordSplit = contentsTest.split()
    contentsKeyWordSplit = contentsKey.split()

    '''
    - In order to create the confusion matrix and get the accuracy score, we have gather the sentiment (positive or negative) on each line of the 
    of the output file from sentiment.py (my-sentiment-answers.txt) and sentiment-test-key.txt
    - This is done by utilizing regex, the regex pattern captures anything that starts with sentiment and ends with a quotation
    - It then traverses each word in the split files to see if the pattern matches any word, if it does match, it appends it to
    a list 
    - This process is done twice, one for my-sentiment-answers.txt and one for sentiment-test-key.txt --> in the end, we have two list of senses: sentTest and sentKey
    - SentTest and SenstKey will be compared to create the confusion matrix and get the accuracy score
    '''

    pattern='sentiment="([^"]*)"'
    sentTest=[]

    for i in contentsTestWordSplit:
        match = re.search(pattern, i)
        if match:
            sent=match.group(1)
            sentTest.append(sent)
    
    

    
    sentKey=[]

    for i in contentsKeyWordSplit:
        match = re.search(pattern, i)
        if match:
            sentK=match.group(1)
            sentKey.append(sentK)
    #print("sent key", sentKey)

    '''
    # Using Pandas to create a confusion matrix to find how accurately positive and negative were identified in my-sentiment-answers.txt
    # Assigning the list sentKey and sentTest list that was created above and set it to Series (1-d Array)
    # Labeling the y_actKey as Actual and y_predTest as Predicted
    # Using crosstab method to create a confusion matrix 
    # Using accuracy_score method to find the accuracy and multipling it by 100 to get a whole number
    # Utilzing Seaborn and matplotlib to generate an easily readible confusion matrix that pops up, while also writing it and the accuracy score to STDOUT 
    '''

    '''
    #In the end, the highest accuracy achieved was 69%, the True Positives was 141, True Negatives was 20, False Negatives was 19, and the False Positive was 52
    #I believe that due to the training set being highly imbalanced as there were 160 occurances of positive tweets and 73 negative tweets, this lead to an increase in false positives
    #   because  the algorithm had trained on more instances of positives than negatives.
    # The baseline accuracy was 68%, again, I believe this is due to the fact that the majority of the Tweets in the training set were positive already and there were not many negatives 
        to be identified in the testing set.
    #A method that I implemented that may have helped with the accuracy was replacing all the website urls to just the word 'websiteLink', this is because when training, I noticed that all of the
        urls were unqiue, and that would mean no match would be found between the testing and the training, hence replacing all of them in the training set and testing set prior to finding the number of positive 
        or negatives, helped reduce the extraneous values in our log dict and sentiment dict. This could have also aided in a better accuracy because instead of ignoring the link because no match would be found, 
        by replacing them, you can take the websiteLink into consideration when determining which word has the highest log value. 
    '''

    acc = accuracy_score(sentKey, sentTest)
    print("Accuracy: ", acc *100)

    y_actKey = pd.Series(sentKey, name='Actual')
    y_predTest= pd.Series(sentTest, name='Predicted')

    df_conf = pd.crosstab(y_actKey, y_predTest)
    sn.heatmap(df_conf, annot=True, fmt='g')
    plt.show()

    print("\n%s" % df_conf)

    



if __name__ == "__main__":
    main(sys.argv)