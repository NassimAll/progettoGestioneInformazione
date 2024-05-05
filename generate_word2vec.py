import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import os
import pandas as pd
from gensim.models import Word2Vec
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
directory = r'C:\Users\sebyl\Desktop\Uni\GestioneInfoProg\FILES'
i = 0
limit = 50000
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
            i += 1
            text = fd.read()
            # aut = fd.readline().replace("[", "").replace("]", "").replace("'", "").replace("\n", "").replace("nan", "")
            # genre = fd.readline().replace("[", "").replace("]", "").replace("'", "").replace("\n", "").replace("nan", "")
            # review = fd.read()
            data.append(preprocessText(text))
            if i >= limit:  break

    #model = Word2Vec(sentences=data)
    model = gensim.models.Word2Vec(data, min_count=1, vector_size=100, window=5, sg=1)
    model.save("Books_word2vec.model")  # save the model
    return model


# # Python program to generate word vectors using Word2Vec
 
# # importing all necessary modules
# from gensim.models import Word2Vec
# import gensim
# from nltk.tokenize import sent_tokenize, word_tokenize
# import warnings
 
# warnings.filterwarnings(action='ignore')
 
 
# #  Reads ‘alice.txt’ file
# sample = open("C:\\Users\\Admin\\Desktop\\alice.txt")
# s = sample.read()
 
# # Replaces escape character with space
# f = s.replace("\n", " ")
 
# data = []
 
# # iterate through each sentence in the file
# for i in sent_tokenize(f):
#     temp = []
 
#     # tokenize the sentence into words
#     for j in word_tokenize(i):
#         temp.append(j.lower())
 
#     data.append(temp)
 
# # Create CBOW model
# model1 = gensim.models.Word2Vec(data, min_count=1,
#                                 vector_size=100, window=5)
 
# # Print results
# print("Cosine similarity between 'alice' " +
#       "and 'wonderland' - CBOW : ",
#       model1.wv.similarity('alice', 'wonderland'))
 
# print("Cosine similarity between 'alice' " +
#       "and 'machines' - CBOW : ",
#       model1.wv.similarity('alice', 'machines'))
 
# # Create Skip Gram model
# model2 = gensim.models.Word2Vec(data, min_count=1, vector_size=100,
#                                 window=5, sg=1)
 
# # Print results
# print("Cosine similarity between 'alice' " +
#       "and 'wonderland' - Skip Gram : ",
#       model2.wv.similarity('alice', 'wonderland'))
 
# print("Cosine similarity between 'alice' " +
#       "and 'machines' - Skip Gram : ",
#       model2.wv.similarity('alice', 'machines'))

# def create_dataset() -> pd.DataFrame:
#     i = 0
#     data = []
#     for filename in os.listdir(directory):
#         with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
#             title = file.readline()
#             author = file.readline().replace("[", "").replace("]", "").replace("'", "").replace("\n", "").replace("nan", "")
#             genre = file.readline().replace("[", "").replace("]", "").replace("'", "").replace("\n", "").replace("nan", "")
#             review = file.read()
#             d = {
#                 'title': title,
#                 "author": author,
#                 "genre": genre, 
#                 "review": review
#             }
#             data.append(d)
#             i = i+1
#         if i > 50000: break

#     df = pd.DataFrame(data)
#     df = df.drop_duplicates()
#     df = df.dropna()

#     return df
    
# if __name__ == "__main__":

#     df = create_dataset()

#     df.to_csv("dataset.csv", index=False)


