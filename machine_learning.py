# -*- coding: utf-8 -*-
import numpy as np
import sys
import random
import json
import pandas

from keras.layers import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.models import Sequential, load_model
from keras.callbacks import ModelCheckpoint

import TweetDataset

def create_model(X, Y):
    print("model create task processing,,,")
    epochs = 2
    batch_size = X.shape[1]
    output_dim = X.shape[2]
    model = Sequential()
    model.add(LSTM(64, return_sequences=False, input_shape=(batch_size, output_dim)))
    model.add(Dense(output_dim, activation='relu'))
    model.compile(loss = 'mean_squared_error', optimizer = 'rmsprop')
    return model

def sampling(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def learning(model, dataset):
    # train the model, output generated text after each iteration
    X = dataset["X"]
    Y = dataset["Y"]
    maxlen = dataset["strmax"]
    text = dataset["alltweet"]
    chars = dataset["chars"]
    char_indices = dataset["char_indices"]
    indices_char = dataset["indices_chars"]
    cb = None


    for iteration in range(1, 60):
        print()
        print('-' * 50)
        print('Iteration', iteration)
        history = model.fit(X, Y, batch_size=128, epochs=1, callbacks=cb)
        start_index = random.randint(0, len(text) - maxlen - 1)

        for diversity in [0.2, 0.5, 1.0, 1.2]:
            print()
            print('----- diversity:', diversity)

            generated = ''
            sentence = text[start_index: start_index + maxlen]
            generated += str(sentence)
            print('----- Generating with seed: "' + str(sentence) + '"')
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
    return model

def save_model_dataset(model, dataset, filename):
    model.save("model/" + filename + "_model.h5")
    print("model saved at" + "model/" + filename + "_model.h5")
    
def open_model_dataset(systemcall):
    model = None
    dataset_dict = {}

    filename = select_file(systemcall)

    # modelとdataset読み込み処理
    try:
        if "-f" in systemcall:
            print(("model load task skipped"))
            raise FileNotFoundError("model load task skipped")
        print("model load from: " + "model/" + filename + "_model.h5")
        model = load_model("model/" + filename + "_model.h5")
        dataset = TweetDataset.TweetDataset("tweetdata/" + filename + "_shaped.csv")
        dataset_dict = dataset.to_dict()
    except (FileNotFoundError, OSError):
        print("model create from dataset")
        dataset = TweetDataset.TweetDataset("tweetdata/" + filename + "_shaped.csv")
        model = create_model(dataset.X, dataset.Y)
        dataset_dict = dataset.to_dict()

    model.summary()
    return model, dataset_dict

def select_file(systemcall):
    # データを選ぶ処理
    filename = ""
    if "tweets" in systemcall:
        filename = "tweets"
    elif "replies" in systemcall:
        filename = "replies"
    elif "rts" in systemcall:
        filename = "rts"
    elif "mini_replies" in systemcall:
        filename = "mini_replies"
    elif "mini_rts" in systemcall:
        filename = "mini_rts"
    else:
        filename = "mini_tweets"
    return filename

if __name__ == "__main__":
    model, dataset = open_model_dataset(sys.argv)
    model = learning(model, dataset)
    save_model_dataset(model, dataset, select_file(sys.argv))
