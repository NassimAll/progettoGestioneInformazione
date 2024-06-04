import scipy
from nltk import word_tokenize
from nltk.corpus import stopwords
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.analysis import StandardAnalyzer
import numpy as np
import os
from gensim.models import Word2Vec
import gensim
from whoosh.scoring import BM25F
from whoosh.qparser import QueryParser, MultifieldParser

directory = r"/Users/nax/Desktop/InvertedIndex"
ix = open_dir(directory)

def preprocessText(text):
    # Tokenization
    tokens = word_tokenize(text)

    # Rimozione della punteggiatura
    tokens = [word for word in tokens if word.isalnum()]

    # Rimozione delle stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    return " ".join(tokens)

def word2vec_score(doc, score, query, model):
    # Calculate cosine similarity of the query and the document
    query_vector = preprocessed_query(query, model)
    doc_vector = generateVector(doc['content'], model)
    similarity = np.dot(query_vector, doc_vector) / (np.linalg.norm(query_vector) * np.linalg.norm(doc_vector))
    return score * similarity

class Word2VecModel(BM25F):
    use_final = True
    query_str = ""
    model = gensim.models.Word2Vec.load("Books_word2vec.model")  # window=5, min_count=5

    def __init__(self):
        super().__init__(B=0.5, K1=1.5)

    def set_query(self, query):
        self.query_str = query

    def final(self, searcher, docnum, score):
        return word2vec_score(searcher.stored_fields(docnum), score, self.query_str, self.model)

#GENERAZIONE DEL VETTORE DEL DOCUMENTO TROVATO PER VALUTARNE LA SIMILARITà CON LA QUERY
def generateVector(content, model):
    dim = len(model.wv.vectors[0])
    words = [word for word in content if word in model.wv]
    if not words:
        return np.zeros(dim)
    else:
        return np.mean([model.wv[word] for word in words], axis=0)

#PREPROCESSING DELLA QUERY E GENERAZIONE DEL VETTORE PER IL CALCOLO DELLA SIMILARITA'
def preprocessed_query(query, model):
    # Create a vector representation from the query
    dim = len(model.wv.vectors[0])
    analyzer = StandardAnalyzer()
    preprocessed_content = [token.text for token in analyzer(query)]
    words = [word for word in preprocessed_content if word in model.wv]
    if not words:
        query_vector = np.zeros(dim)
    else:
        query_vector = np.mean([model.wv[word] for word in words], axis=0)
    return query_vector

def query():
    query_text = str(input("Insert the query: "))
    weighting_model = Word2VecModel
    weighting_model.set_query(Word2VecModel,query_text)
    with ix.searcher(weighting=weighting_model) as searcher:
        parser = QueryParser(fieldname="content", schema=ix.schema)
        searchquery = parser.parse(preprocessText(query_text))
        results = searcher.search(searchquery, limit=10, terms=True)
        if len(results) == 0:
            print("No results found")
            return
        for hit in results:
            print(f"File: {hit['path']}")
            print(f"Score: {hit.score}")
            print("---------------\n")

if __name__ == "__main__":
    while True:
        print("========================================================")
        print("Choose what to do...")
        print("0. Exit")
        print("1. Search")
        print("========================================================")
        choice = int(input(""))
        if choice == 0:
            break
        elif choice == 1:
            query()