import numpy as np
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense,Embedding,LSTM,SpatialDropout1D,Dropout
from keras.utils.np_utils import to_categorical
from numpy.random import permutation
import tensorflow as tf
import time as t
#stopwords=set(stopwords.words("english"))
def get_data():
    df1=pd.read_csv("C:/Users/3301/Desktop/Files/non_bid_names.csv",encoding='unicode_escape')
    df2=pd.read_csv("C:/Users/3301/Desktop/Files/bid_names.csv")
    X,Y=[],[]
    df2.dropna(inplace=True)
    df1.dropna(inplace=True)
    for items in df2.iloc[1:,0]:
        X.append(items)
    for items in df1.iloc[0:,0]:
        X.append(items)

    for items in df2.iloc[1:,1]:
        Y.append(int(items))
    for items in df1.iloc[0:,1]:
        Y.append(int(items))

    X=np.array(X,dtype='object')
    Y=np.array(Y,dtype='int32')
    perm=permutation(len(X))
    X=X[perm]
    Y=Y[perm]
    return X,Y

def prepare_train_test_model(X,Y):
    vocab_size=50000
    embedding_dim=100
    max_length=250
    trunc_type='post'
    padding_type='post'
    oov_tok="<OOV>"
    training_size=24505
    training_sentences=X[:training_size]
    testing_sentences=X[training_size:]
    training_labels=Y[:training_size]
    testing_labels=Y[training_size:]
    tokenizer=Tokenizer(num_words=vocab_size,oov_token=oov_tok,filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~')
    tokenizer.fit_on_texts(training_sentences)
    training_sequences=tokenizer.texts_to_sequences(training_sentences)
    training_padded=pad_sequences(training_sequences,maxlen=max_length,padding=padding_type,truncating=trunc_type)
    testing_sequences=tokenizer.texts_to_sequences(testing_sentences)
    testing_padded=pad_sequences(testing_sequences,maxlen=max_length,padding=padding_type,truncating=trunc_type)
    model=tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size,embedding_dim,input_length=max_length),
    tf.keras.layers.LSTM(100,dropout=0.2,recurrent_dropout=0.2),
    tf.keras.layers.Dense(3,activation='softmax')
    ])
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()
    num_epochs=10
    history=model.fit(training_padded,training_labels,epochs=num_epochs,validation_data=(testing_padded, testing_labels), verbose=2)
    #sequencer=tokenizer.texts_to_sequences(testing_sequences)
    #padded=pad_sequences(sequencer,maxlen=max_length,padding=padding_type,truncating=trunc_type)
    #print(model.predict(padded))

if __name__=='__main__':
    X,Y=get_data()
    prepare_train_test_model(X,Y)