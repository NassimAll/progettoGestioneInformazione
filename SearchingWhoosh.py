from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import scoring
import os, os.path

ix = open_dir(r"C:\Users\sebyl\Desktop\Uni\GestioneInfoProg\progettoGestioneInformazione\index")

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
                parser = QueryParser(fieldname="review", schema=ix.schema)
                searchstring = input("Insert a string \n")
                query = parser.parse(searchstring)

            print("Searching...\n")
            
            
            results = searcher.search(query, limit = 10, terms = True)
            if len(results) == 0:
                print("Empty result!!")
            else:
                print(results)
                for hit in results:
                    print("\n")
                    print(hit)
                    print("Score: ", hit.score)
                    print("Rank: ", hit.rank)
                    print("Document number: ", hit.docnum)
                    print("\n")
