# -*- coding: utf-8 -*-
import numpy as np

from keras.layers import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.models import Sequential

import model_shaper as m_shape

def create_model(X, Y):
    # Sequentialモデルの最初のレイヤーとして
    epochs = 2
    batch_size = X.shape[0] * X.shape[1] * X.shape[2]
    print(X.shape)
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_dim=X.shape[2], input_length=X.shape[1]))
    model.add(LSTM(32, return_sequences=True))
    model.add(Dense(20))
    model.add(Activation("linear"))
    model.compile(loss = 'mean_squared_error', optimizer = 'adam')
    return model


if __name__ == "__main__":
    dir = ""
    # load_csv <0:RTtweet,0:normaltweet,0<:reply
    rts = m_shape.load_csv(dir, -1)
    tweets = m_shape.load_csv(dir, 0)
    replies = m_shape.load_csv(dir, 1)
    X, Y = m_shape.labering(tweets)
    create_model(X, Y)
