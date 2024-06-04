from nltk import word_tokenize
from nltk.corpus import stopwords
from whoosh.index import create_in, open_dir
from whoosh.fields import *
import os

directory = r'/Volumes/SSDEsterno_Nasso/PROGETTO_GESTIONE/FILESFULL'
schema = Schema(path=ID(stored=True, analyzer=None), content=TEXT(analyzer=None, stored=True))

def preprocessText(text):
    # Tokenization
    tokens = word_tokenize(text)

    # Rimozione della punteggiatura
    tokens = [word for word in tokens if word.isalnum()]

    # Rimozione delle stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    return tokens


def generateIndex():
    #DEFINISCO DOVE CREARE L'INDEX
    ix = create_in(r"/Users/nax/Desktop/InvertedIndex", schema)
    writer = ix.writer()
    c = 1
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            print(c)
            content = file.read().replace("[", "").replace("]", "").replace("'", "").replace("\n", "").replace("nan", "")
            preprocessed_content = preprocessText(content)
            writer.add_document(path=os.path.join(directory, filename), content=preprocessed_content)
            c = c + 1

    print("commit....")
    writer.commit()
    print("commit eseguito")
    return

if __name__ == "__main__":
    generateIndex()