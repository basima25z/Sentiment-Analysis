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

def main(argv):
    testFile = os.path.basename(sys.argv[1])
    keyFile = os.path.basename(sys.argv[2])

    openTestFile = open(testFile, "r")
    contentsTest = openTestFile.read().lower()

    openKeyFile = open(keyFile, "r")
    contentsKey = openKeyFile.read().lower()

    contentsTestWordSplit = contentsTest.split()
    contentsKeyWordSplit = contentsKey.split()

    pattern='sentiment="([^"]*)"'
    sentTest=[]

    for i in contentsTestWordSplit:
        match = re.search(pattern, i)
        if match:
            sent=match.group(1)
            sentTest.append(sent)
    
    #print("sent test", sentTest)

    
    sentKey=[]

    for i in contentsKeyWordSplit:
        match = re.search(pattern, i)
        if match:
            sentK=match.group(1)
            sentKey.append(sentK)
    #print("sent key", sentKey)

    acc = accuracy_score(sentKey, sentTest)
    print("Accuracy: ", acc *100)

    y_actKey = pd.Series(sentKey, name='Actual')
    y_predTest= pd.Series(sentTest, name='Predicted')

    df_conf = pd.crosstab(y_actKey, y_predTest)
    sn.heatmap(df_conf, annot=True, fmt='g')
    #sns.heatmap(table2,annot=True,cmap='Blues', fmt='g')
    plt.show()

    print("\n%s" % df_conf)

    



if __name__ == "__main__":
    main(sys.argv)