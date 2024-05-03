from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import scoring
import os, os.path
from transformers import AutoModelForSequenceClassification, AutoConfig
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
max_length = 512
ix = open_dir(r"C:\Users\sebyl\Desktop\Uni\GestioneInfoProg\progettoGestioneInformazione\index")

def sentiment_score(doc, score):
    return score * doc['sentimentValue']


class SentimentBM25F(scoring.BM25F):
    use_final = True

    def final(self, searcher, docnum, score):
        return sentiment_score(searcher.stored_fields(docnum), score)


def extractQuerySentiment(querystring):
    encoded_input = tokenizer(querystring, max_length=max_length, return_tensors='pt', truncation=True)

    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    tmp_dict = {
        'negative': scores[0],
        'neutral': scores[1],
        'positive': scores[2]
    }

    max_score = max(tmp_dict.values())
    max_type = list(tmp_dict.keys())[list(tmp_dict.values()).index(max_score)]

    return max_type

def sentimentChoice():
    while True:
        print("What sentiment are you looking for? ")
        print("1.Positive")
        print("2.Neutral")
        print("3.Negative")
        choice = int(input(""))
        if choice == 1: return "positive"
        elif choice == 2: return "neutral"
        elif choice == 3: return "negative"
        
        print("You insert the wrong number, retry")

def showResult(res):
     for hit in res:
        print(hit)
        print("Score: ", hit.score)
        print("Rank: ", hit.rank)
        print("Document number: ", hit.docnum)
        print("\n")

def print_menu():
    print("========================================================")
    print("Choose what are you searching for...")
    print("0. Exit")
    print("1. Book title")
    print("2. Book author")
    print("3. Comments in the review")
    print("========================================================")
    choice = int(input(""))
    return choice

def print_menu_model():
    print("========================================================")
    print("Choose the ranking model...")
    print("1. Default BM25F")
    print("2. TF_IDF")
    print("3. Frequency")
    print("4. BM25F + Sentiment analysis")
    print("========================================================")
    choice = int(input(""))
    if choice == 1:
        model = scoring.BM25F()
        return model
    elif choice == 2:
        model = scoring.TF_IDF()
        return model
    elif choice == 3:
        model = scoring.Frequency()
        return model
    elif choice == 4:
        model = SentimentBM25F
        return model

if __name__ == "__main__":
    while(True):
        choice = print_menu()
        model = print_menu_model()
        with ix.searcher(weighting = model) as searcher:
            if choice == 0:
                break
            elif choice == 1:
                parser = QueryParser(fieldname="title", schema=ix.schema)
                searchstring = input("Insert the title of the book \n")
                query = parser.parse(searchstring)
            elif choice == 2:
                parser = QueryParser(fieldname="author", schema=ix.schema)
                searchstring = input("Insert the author of the book \n")
                query = parser.parse(searchstring)
            elif choice == 3:
                if model == SentimentBM25F:
                    parser = MultifieldParser(["review", "sentimentType"], schema=ix.schema)
                    query_str = input("Insert a string \n")
                    sent = sentimentChoice()
                    searchstring = "\"" + query_str + "\"" + " \"" + sent + "\""
                    query = parser.parse(searchstring)
                else: 
                    parser = QueryParser(fieldname="review", schema=ix.schema)
                    searchstring = input("Insert a string \n")
                    query = parser.parse(searchstring)

            print("Searching...\n")
            
            results = searcher.search(query, limit = 10, terms = True)
            if len(results) == 0:
                print("Empty result!!")
                corrected = searcher.correct_query(query, searchstring)
                if corrected.query != query:
                    print(f"Did you mean: {corrected.string} (y/n)")
                    ans = input().lower()
                    if ans == "y": 
                        results = searcher.search(corrected.query, limit = 10, terms = True)
                        showResult(results)
            else:
                showResult(results)
