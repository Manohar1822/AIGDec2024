import aqgFunction

import sys

import pymongo

from pymongo import MongoClient

import numpy as np

import pandas as pd

client = MongoClient('mongodb://127.0.0.1:27017/')

db = client['organizationsDB']

collection=db['paragraphs']


import openai

openai.api_key='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'

import time

# Sleep for 30 seconds

data=collection.find({'generated': False})
count=0
for document in data:
    count+=1
    if(count%2==0):
        time.sleep(30)
    
    paragraph=document['paragraph']
    easy=document['easy']
    medium=document['medium']
    hard=document['hard']
    
    
    messages=[
        {"role": "system", "content": "You are question and answer creator from paragraph, and you create descriptive and subjective questions and answers according to paragraph and given conditions and start each question by ***. Easy level is 1 to 10 sentece, Medium level is 7 to 20 sentences and Hard level is 20 sentences and above"}
    ]

    #print(question)
    message=paragraph+"\n\nFrom above Paragraph only, Generate Level wise "+easy+" easy question and its answer, "+medium+" medium questions and its answer and "+hard+" hard questions and answers from above paragraph. Easy level is 1 to 10 sentece, Medium level is 7 to 20 sentences and Hard level is 20 sentences and above. Note: Do not write a single comment or words apart from questions and answers and start each question after writing ***"

    messages.append(
        {"role": "user", "content": message}
    )
    resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages
    )
    reply="Below are questions generated from above paragraph \n "+resp.choices[0].message.content
    

    collection.update_one({'_id': document['_id']}, {'$set': {'genQues': reply, 'generated':True}})
    print(f"Open AI generated as: {reply}")
    messages.append({"role": "assistant", "content": reply})







# Main Function
# def main():
#     # Create AQG object
#     aqg = aqgFunction.AutomaticQuestionGenerator()

#     inputTextPath = "input file path -- ?? ../DB/db.txt"
#     readFile = open("DB/db01.txt", 'r+', encoding="utf8")
#     #readFile = open(inputTextPath, 'r+', encoding="utf8", errors = 'ignore')

#     inputText = readFile.read()
#     #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''

#     questionList = aqg.aqgParse(inputText)
#     aqg.display(questionList)

#     #aqg.DisNormal(questionList)

#     return 0


# # Call Main Function
# if __name__ == "__main__":
#     main()

