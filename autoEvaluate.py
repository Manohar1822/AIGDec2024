import sys



import pymongo

from pymongo import MongoClient

import numpy as np

import pandas as pd

import nltk


from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.decomposition import TruncatedSVD

from sentence_transformers import SentenceTransformer




# Load pre-trained BERT model

model = SentenceTransformer('bert-base-nli-mean-tokens')





client = MongoClient('mongodb://127.0.0.1:27017/')

db = client['organizationsDB']

collection=db['answers']

data = collection.find()

# for document in data:

#     #print(document['question']['maxMarks'])

#     marks=0

#     # Load model answer

#     model_answer = document['question']['solution']
#     model_answerForGPT=document['question']['solution']

#     # Load student answer

#     student_answer = document['answer']
#     student_answerForGPT = document['answer']
#     # Preprocess model answer and student answer

#     stop_words = set(stopwords.words('english'))

#     model_answer = ' '.join([word.lower() for word in model_answer.split() if word.lower() not in stop_words])

#     student_answer = ' '.join([word.lower() for word in student_answer.split() if word.lower() not in stop_words])



#     # Calculate LSA similarity score

#     vectorizer = TfidfVectorizer()

#     lsa = TruncatedSVD(n_components=1, n_iter=100)

#     model_tfidf = vectorizer.fit_transform([model_answer, student_answer])

#     model_lsa = lsa.fit_transform(model_tfidf)

#     lsa_score = np.dot(model_lsa[0], model_lsa[1]) # matches the vecors which are shadowing other. dot here is dot product of vecors and give magnitude of vector 1 in direction of vector 2



#     # Calculate BERT similarity score

#     model_embedding = model.encode([model_answer])

#     #print(model_embedding)

#     student_embedding = model.encode([student_answer])

#     #print(student_embedding)

#     bert_score = np.dot(model_embedding[0], student_embedding[0])

#     outOf=np.dot(model_embedding[0],model_embedding[0])

    

#     LsaPer=lsa_score*100

#     BertPer=bert_score*100/outOf
#     bert_scor = np.dot(student_embedding[0],model_embedding[0])

#     outO=np.dot(student_embedding[0],student_embedding[0])

#     BertPe=bert_scor*100/outO

#     if ((LsaPer+BertPer)/2)<75:

#         if((LsaPer+BertPer)/2)<60:

#             marks=0

#         else:

#             marks=(((LsaPer+BertPer+BertPe)/3))*document['question']['maxMarks']/100

#     elif BertPer<85:

#         marks=(((BertPer-85)+25)/30)*document['question']['maxMarks']/100

#     else:

        

#         marks=((LsaPer+BertPer+BertPe)/3)*document['question']['maxMarks']/100

#     print(round(marks,2))
#     print("BertPercent= ",BertPer)
#     print("LSAPer= ",LsaPer)
#     collection.update_one({'_id': document['_id']}, {'$set': {'obtainMarks': marks}})

    
    

    

print("AutoEvaluated all answers Successfully")

#
#
#
#
#Integrating openAI
# for document in data:
#     collection.update_one({'_id': document['_id']}, {'$set': {'obtainMarks': -1}})

import re

def extract_decimal_numbers(input_string):
    # Define a regular expression pattern to match decimal numbers
    decimal_pattern = r'\d+\.\d+|\d+'

    # Use re.findall to find all occurrences of the pattern in the input string
    decimal_numbers = re.findall(decimal_pattern, input_string)

    # Convert the matched strings to actual decimal numbers
    decimal_numbers = [float(number) for number in decimal_numbers]

    return decimal_numbers

import openai

openai.api_key='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'

import time

# Sleep for 30 seconds

data=collection.find({'obtainMarks': -1})
count=0
for document in data:
    count+=1
    if(count%2==0):
        time.sleep(30)
    marks=0
    model_answerForGPT=document['question']['solution']
    student_answerForGPT = document['answer']
    question=document['question']['question']
    messages=[
        {"role": "system", "content": "Your reply should be marks only and no any extra words and explaination. You are a helpful assistant to evaluate the student answer from model answer and your krnowledge that you have for given question and then assign marks out of 100."}
    ]

    #print(question)
    message="Return only marks and no any single words. Evaluate Student Answer with reference to model answer and your knowledge gor given question out of 100 Marks. Question: "+question+"\nStudent Answer: "+student_answerForGPT+". \n Model answer: "+model_answerForGPT

    messages.append(
        {"role": "user", "content": message}
    )
    resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages
    )
    reply=resp.choices[0].message.content
    
    reply = extract_decimal_numbers(reply)
    
    marks=(int(reply[0])*document['question']['maxMarks'])/100
    if(student_answerForGPT=="NA"):
        marks=0
    collection.update_one({'_id': document['_id']}, {'$set': {'obtainMarks': marks}})
    print(f"Open AI evaluated as: {reply}")
    messages.append({"role": "assistant", "content": reply})