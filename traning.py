import stanza
import json
import requests
import random
import numpy as np
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
print("Succesfully import library")

#* Initialize variable
words = []
classes = []
documents = []
ignore_words = ['?', '!']
nlp = stanza.Pipeline('id', processors='tokenize,lemma')
print("Succesfully initialize variable")

#* Get data from strapi and write to json file
res = requests.get('https://chatbot-dashboard.fly.dev/api/intents?sort=id&pagination[pageSize]=100', headers={
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 01cf9c34be68c91e2a4945c0ffc0e842e51fcf8591c065b68514fde86a6c0049837942cf6a2691770529f784c41d2685a7e5ca2f8e55b8bbff6f7cf8e4247d4af3dbb609d3a519dcbeb600a4060fd43223410d3db0cb0cd92d80c5aef6acacfb175ffcfb20eb633102226981c165cda26d3d035ddb42049c6c7d03dbaab8a6c5'
})
res_data = res.json()['data']
json_data = json.dumps(res_data, indent=2)
with open("data.json", "w") as outfile:
    outfile.write(json_data)
print("Succesfully load data from database and write to json file")

#* create word and class file
for data in res_data:
    for pattern in data["attributes"]["patterns"]:
        doc = nlp(pattern.lower())
        w = [word.lemma for sent in doc.sentences for word in sent.words if word.text not in ignore_words]
        words.extend(w)
        documents.append((w, data["attributes"]["tag"]))
        if data["attributes"]["tag"] not in classes:
            classes.append(data["attributes"]["tag"])
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))
pickle.dump(words,open('texts.pkl','wb')) 
pickle.dump(classes,open('labels.pkl','wb'))
print("Succesfully create words and classes file")

#* create our training data
training = []
#* create an empty array for our output
output_empty = [0] * len(classes)
for doc in documents:
    bag = []
    pattern_words = doc[0]
    
    docs = nlp(" ".join(pattern_words).lower())
    pattern_words = [word.lemma for sent in docs.sentences for word in sent.words if word.text not in ignore_words]

    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])
random.shuffle(training)
training = np.array(training, dtype="object")
#* create train and test lists
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Succesfully training data")

#* create ANN models
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
print("Succesfully create ANNs model")

#* Save model
model.save('models.h5', hist)
print("Succesfully save ANNs model")