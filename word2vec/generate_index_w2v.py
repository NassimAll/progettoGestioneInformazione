from nltk import word_tokenize
from nltk.corpus import stopwords
from whoosh.index import create_in, open_dir
from whoosh.fields import *
import os

directory = r'/Volumes/SSDEsterno_Nasso/PROGETTO_GESTIONE/FILES'
schema = Schema(path=ID(stored=True, analyzer=None), vectors=TEXT(analyzer=None), content=TEXT(analyzer=None, stored=True))


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
            #print(content)
            preprocessed_content = preprocessText(content)
            #print(preprocessText(content))
            writer.add_document(path=os.path.join(directory, filename), content=preprocessed_content)
            #print(preprocessed_content)
            # words = [word for word in preprocessed_content if word in model.wv]
            # if not words:
            #     #docs_vector[filename] = np.zeros(dim)
            #     #writer.add_document(path=os.path.join(directory, filename), vectors=' '.join(map(str, np.zeros(dim))), content=preprocessed_content)
            #     writer.add_document(path=os.path.join(directory, filename), content=preprocessed_content)
            # else:
            #     #docs_vector[filename] = np.mean([model.wv[word] for word in words], axis=0)
            #     #print(type(np.mean([model.wv[word] for word in words], axis=0)))
            #     #tmp = ' '.join(map(str, np.mean([model.wv[word] for word in words], axis=0)))
            #     #print(' '.join(map(str, np.mean([model.wv[word] for word in words], axis=0))))
            #     #print(np.ndarray(map(np.float32, tmp.split(" "))) )
            #     #writer.add_document(path=os.path.join(directory, filename), vectors=' '.join(map(str, np.mean([model.wv[word] for word in words], axis=0))), content=preprocessed_content)
            #     writer.add_document(path=os.path.join(directory, filename), content=preprocessed_content)
            c = c + 1

    print("commit....")
    writer.commit()
    print("commit eseguito")
    return

if __name__ == "__main__":
    generateIndex()