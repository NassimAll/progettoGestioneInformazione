from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path

ix = open_dir(r"C:\Users\sebyl\Desktop\Uni\GestioneInfoProg\index")

def print_menu():
    print("========================================================")
    print("Choose what are you searching for...")
    print("0. Null")
    print("1. Book title")
    print("2. Book author")
    print("3. Comments in the review")
    print("========================================================")
    choice = int(input(""))
    return choice

if __name__ == "__main__":
    while(True):
        choice = print_menu()
        searcher = ix.searcher()
        if choice == 0:
            break
        elif choice == 1:
            parser = QueryParser("title", schema=ix.schema)
            searchstring = input("Insert the title of the book \n")
            query = parser.parse(searchstring)
        elif choice == 2:
            parser = QueryParser("author", schema=ix.schema)
            searchstring = input("Insert the author of the book \n")
            query = parser.parse(searchstring)
        elif choice == 3:
            parser = QueryParser("review", schema=ix.schema)
            searchstring = input("Insert a string \n")
            query = parser.parse(searchstring)
        
        
        results = searcher.search(query, limit = 10, terms = True)
        if len(results) == 0:
            print("Empty result!!")
        else:
            #print(results[0])
            for hit in results:
                print(hit)
                print("the Score", hit.score)
                print("the rank", hit.rank)
                print("the document number", hit.docnum)


