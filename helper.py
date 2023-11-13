import config

import stanza
import numpy as np
import json
import pickle
import random
from keras.models import load_model
import requests

model = load_model('models.h5')
intents = json.loads(open('data.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))

nlp = stanza.Pipeline('id', processors='tokenize,lemma')

def clean_up_sentence(sentence):
    doc = nlp(sentence.lower())
    sentence_words = [word.lemma for sent in doc.sentences for word in sent.words]
    return sentence_words

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    #* filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    # print(res)
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # print(results)
    #* sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(ints, intents):
    tag = ints[0]['intent']
    for i in intents:
        if(i['attributes']['tag']== tag):
            result = random.choice(i['attributes']['responses'])
            break
    return result

def get_answer(msg):
    ints = predict_class(msg, model=model)
    res = get_response(ints=ints, intents=intents)
    return res

async def insert_to_logs(question, answer):
    req_data = {
        'data': {
            'question': question,
            'answer': answer
        }
    }
    res = requests.post(f'{config.SERVER_URL}/logs', json=req_data, headers=config.HEADERS)
    return res


#! for testing only
# questions = "wgwgwg"
# print("Pertanyaan")
# print(questions)
# print("Jawaban")
# print(get_answer(questions))