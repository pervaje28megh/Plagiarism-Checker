from flask import Flask, request, render_template, Markup
import re
import math
import webbrowser
from threading import Timer
import numpy as np

app = Flask("__name__")

q = ""
pred=['No Plagiarism Detected','Plagiarism Detected']

@app.route("/")
def loadPage():
    return render_template('index.html', query="")

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

@app.route("/", methods=['POST'])
def cosineSimilarity():
    try:
        universalSetOfUniqueWords = []
        matchPercentage = 0

        ####################################################################################################

        inputQuery = request.form['query']
        lowercaseQuery = inputQuery.lower()

        queryWordList = re.sub("[^\w]", " ",lowercaseQuery).split()            #Replace punctuation by space and split

        for word in queryWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        ####################################################################################################

        fd = open("database1.txt", "r")
        database1 = fd.read().lower()

        databaseWordList = re.sub("[^\w]", " ",database1).split()    #Replace punctuation by space and split

        for word in databaseWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        ####################################################################################################

        queryTF = []
        databaseTF = []

        for word in universalSetOfUniqueWords:
            queryTfCounter = 0
            databaseTfCounter = 0

            for word2 in queryWordList:
                if word == word2:
                    queryTfCounter += 1
            queryTF.append(queryTfCounter)

            for word2 in databaseWordList:
                if word == word2:
                    databaseTfCounter += 1
            databaseTF.append(databaseTfCounter)

        dotProduct = 0
        for i in range (len(queryTF)):
            dotProduct += queryTF[i]*databaseTF[i]

        queryVectorMagnitude = 0
        for i in range (len(queryTF)):
            queryVectorMagnitude += queryTF[i]**2
        queryVectorMagnitude = math.sqrt(queryVectorMagnitude)

        databaseVectorMagnitude = 0
        for i in range (len(databaseTF)):
            databaseVectorMagnitude += databaseTF[i]**2
        databaseVectorMagnitude = math.sqrt(databaseVectorMagnitude)

        match = (float)(dotProduct / (queryVectorMagnitude * databaseVectorMagnitude))
        matchPercentage = match*100
        res=math.floor(match + 0.5)
        fin_result=pred[res]

        output = "Input query text matches %0.02f%% with the text in database<br/>%s" % (matchPercentage, fin_result)
        output = Markup(output)
        return render_template('index.html', query=inputQuery, output=output)
    except Exception as e:
        output = "Please Enter Valid Data"
        return render_template('index.html', query=inputQuery, output=output)

if __name__ == "__main__":
      Timer(1, open_browser).start()
      app.run(port=5000)
