import torch
import numpy as np
import json

from nltk_utils import bag_of_words, tokenize, stem
from model import NeuralNet

with open('intents.json', 'r') as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

def get_response(sentence, user_data):
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    for intent in intents['intents']:
        if intent['tag'] == tag:
            if 'context_set' in intent:
                if 'context_filter' in intent:
                    if user_data.get(intent['context_filter']) == intent['context_filter_value']:
                        return np.random.choice(intent['responses'])
                else:
                    user_data[intent['context_set']] = intent['context_set_value']
            return np.random.choice(intent['responses'])

    return "I'm sorry, I'm not sure how to help with that."
