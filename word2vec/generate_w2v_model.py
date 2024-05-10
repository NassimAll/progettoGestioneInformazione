import scipy

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.analysis import StandardAnalyzer
import numpy as np
from nltk.corpus import stopwords
import os
from gensim.models import Word2Vec
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize

directory = r'/Volumes/SSDEsterno_Nasso/PROGETTO_GESTIONE/FILES'
data = []

def preprocessText(text):
    # Tokenization
    tokens = word_tokenize(text)

    # Rimozione della punteggiatura
    tokens = [word for word in tokens if word.isalnum()]

    # Rimozione delle stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    return tokens


def generate_w2v():
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), 'r', encoding='utf-8') as fd:
            text = fd.read()
            txt = preprocessText(text)
            print(txt)
            data.append(txt)

    model = gensim.models.Word2Vec(data, vector_size=100, window=5, sg=1, min_count=5, workers=4)
    model.save("Books_word2vec.model")  # save the model
    return model

if __name__ == "__main__":
    generate_w2v()
    # model = gensim.models.Word2Vec.load("Books_word2vec.model")  # load the model
    # print(model)
    #generateIndex()

