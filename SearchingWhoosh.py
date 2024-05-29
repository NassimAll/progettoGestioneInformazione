from nltk import word_tokenize
from nltk.corpus import stopwords
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser
from whoosh import scoring
import os, os.path
from transformers import AutoModelForSequenceClassification, AutoConfig
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
Roberta_model = AutoModelForSequenceClassification.from_pretrained(MODEL)
max_length = 512
#ix = open_dir(r"C:\Users\sebyl\Desktop\Uni\GestioneInfoProg\progettoGestioneInformazione\index")
ix = open_dir("/Users/nax/Desktop/index")
#Variabile per rselezionare il sentimento
searchSentiment = ""

'''
    Preprocess della query per trasfomarla da natural language --> query language
'''
def preprocessText(text):
    # Tokenization
    tokens = word_tokenize(text)

    # Rimozione della punteggiatura
    tokens = [word for word in tokens if word.isalnum()]

    # Rimozione delle stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    return " ".join(tokens)

'''
    sentiment_score --> funzione che ricalcola lo score di un documento 
    class Sentiment BM25F --> Ridefiniamo il modello del BM25 modificando il ranking in modo che 
    tenga conto del valore di sentimento del documento 
'''
def sentiment_score(doc, score, sent):
    return score * doc[sent]

class SentimentBM25F(scoring.BM25F):
    use_final = True
    sent = ""

    def setSentiment(self, sent):
        self.sent = sent

    def final(self, searcher, docnum, score):
        return sentiment_score(searcher.stored_fields(docnum), score, self.sent)

'''
    Funzione che viene utilizzata per automatizzare il search engine che lavora con la sentiment analysis
    in modo da ricavare il sentimento dalla query senza richiedere all'utente alcuna interazione
'''
def extractQuerySentiment(querystring):
    encoded_input = tokenizer(querystring, max_length=max_length, return_tensors='pt', truncation=True)

    output = Roberta_model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    tmp_dict = {
        'negative': scores[0],
        'neutral': scores[1],
        'positive': scores[2]
    }

    max_score = max(tmp_dict.values())
    max_type = list(tmp_dict.keys())[list(tmp_dict.values()).index(max_score)]
    print(f"sentiment: {max_type}; score: {max_score}")
    return max_type

'''
Stampa menu di scelta sentiment
'''
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

#Stampa dei risultati 
def showResult(res, sent):
     for hit in res:
        print(hit["path"])
        if sent != "":
            print("neutral - Sentiment value: ", hit["neutral"])
            print("positive - Sentiment value: ", hit["positive"])
            print("negative - Sentiment value: ", hit["negative"])
        print("Score: ", hit.score)
        print("Rank: ", hit.rank)
        print("Document number: ", hit.docnum)
        print("\n")

#Stampa menu di ricerca
def print_menu():
    print("========================================================")
    print("Choose what are you searching for...")
    print("0. Exit")
    print("1. Book title")
    print("2. Book author")
    print("3. Genre")
    print("4. Comments in the review")
    print("========================================================")
    choice = int(input(""))
    return choice

#stampa scelta dei modelli 
def print_menu_model():
    print("========================================================")
    print("Choose the ranking model...")
    print("1. Default BM25F")
    print("2. TF_IDF")
    print("3. Frequency")
    print("4. BM25F + Sentiment analysis ")
    print("5. BM25F + Auto Sentiment analysis ")
    print("========================================================")
    choice = int(input(""))
    if choice == 1:
        model = scoring.BM25F()
        return (choice, model)
    elif choice == 2:
        model = scoring.TF_IDF()
        return (choice, model)
    elif choice == 3:
        model = scoring.Frequency()
        return (choice, model)
    elif choice == 4 or choice == 5:
        model = SentimentBM25F
        return (choice, model)
    

if __name__ == "__main__":
    while(True):
        searchSentiment = ""
        choice = print_menu()
        (Modelchoice, model) = print_menu_model()
        with ix.searcher(weighting = model) as searcher:
            if choice == 0:
                break
            elif choice == 1:   #Search the title
                parser = QueryParser(fieldname="title", schema=ix.schema)
                searchstring = input("Insert the title of the book \n")
                if Modelchoice == 4:    #Check if want to search a sentiment
                        searchSentiment = sentimentChoice()
                        SentimentBM25F.setSentiment(SentimentBM25F, searchSentiment)
                query = parser.parse(searchstring)
            elif choice == 2:   #Search the author
                parser = QueryParser(fieldname="author", schema=ix.schema)
                searchstring = input("Insert the author of the book \n")
                if Modelchoice == 4:    #Check if want to search a sentiment
                        searchSentiment = sentimentChoice()
                        SentimentBM25F.setSentiment(SentimentBM25F, searchSentiment)
                query = parser.parse(searchstring)
            elif choice == 3:   #Search the genre
                parser = QueryParser(fieldname="genre", schema=ix.schema, group=qparser.OrGroup)
                searchstring = input("Insert the genre of the book \n")
                if Modelchoice == 4:    #Check if want to search a sentiment
                        searchSentiment = sentimentChoice()
                        SentimentBM25F.setSentiment(SentimentBM25F, searchSentiment) 
                query = parser.parse(searchstring)
            elif choice == 4:   #Search for a specific in the review
                parser = QueryParser(fieldname="review", schema=ix.schema)
                query_str = input("Insert a string \n")
                searchstring = preprocessText(query_str)
                print(searchstring)
                if model == SentimentBM25F:
                    if Modelchoice == 4:    #Manual sentiment choice
                        print("MANUAL SENTIMENT:")
                        searchSentiment = sentimentChoice()
                        SentimentBM25F.setSentiment(SentimentBM25F, searchSentiment)
                    elif Modelchoice == 5:  #Automatic sentiment analysis of the query
                        print("AUTO SENTIMENT EVALUATION:")
                        searchSentiment = extractQuerySentiment(query_str)
                        SentimentBM25F.setSentiment(SentimentBM25F, searchSentiment)                
                query = parser.parse(searchstring)

            print("Searching...\n")
            
            results = searcher.search(query, limit = 50, terms = True)
            if len(results) == 0:
                print("Empty result!!")
                corrected = searcher.correct_query(query, searchstring)
                if corrected.query != query:    #Check if the query can be corrected
                    print(f"Did you mean: {corrected.string} (y/n)")
                    ans = input().lower()
                    if ans == "y": 
                        results = searcher.search(corrected.query, limit = 50, terms = True)
                        showResult(results, searchSentiment)
            else:
                showResult(results, searchSentiment)
