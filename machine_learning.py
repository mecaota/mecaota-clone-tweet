# -*- coding: utf-8 -*-
import numpy as np
import sys
import random

from keras.layers import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.models import Sequential

import model_shaper as m_shape

def create_model(X, Y):
    epochs = 2
    batch_size = X.shape[1]
    output_dim = X.shape[2]
    model = Sequential()
    model.add(LSTM(64, return_sequences=False, input_shape=(batch_size, output_dim)))
    model.add(Dense(output_dim, activation="linear"))
    model.compile(loss = 'mean_squared_error', optimizer = 'adam')
    return model

def sampling(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def learning(model, X, Y):
    # train the model, output generated text after each iteration
    maxlen = X.shape[1]
    text = ""

    for iteration in range(1, 60):
        print()
        print('-' * 50)
        print('Iteration', iteration)
        model.fit(X, Y, batch_size=128, epochs=1)
        start_index = random.randint(0, len(text) - maxlen - 1)

        for diversity in [0.2, 0.5, 1.0, 1.2]:
            print()
            print('----- diversity:', diversity)

            generated = ''
            sentence = text[start_index: start_index + maxlen]
            generated += sentence
            print('----- Generating with seed: "' + sentence + '"')
            sys.stdout.write(generated)

            for i in range(140):
                x = np.zeros((1, maxlen, len(chars)))
                for t, char in enumerate(sentence):
                    x[0, t, char_indices[char]] = 1.

                preds = model.predict(x, verbose=0)[0]
                next_index = sampling(preds, diversity)
                next_char = indices_char[next_index]

                generated += next_char
                sentence = sentence[1:] + next_char

                sys.stdout.write(next_char)
                sys.stdout.flush()
            print()

if __name__ == "__main__":
    dir = ""
    # load_csv <0:RTtweet,0:normaltweet,0<:reply
    rts = m_shape.load_csv(dir, -1)
    tweets = m_shape.load_csv(dir, 0)
    replies = m_shape.load_csv(dir, 1)
    X, Y = m_shape.labering(tweets)
    model = create_model(X, Y)
    result = learning(model, X, Y)
