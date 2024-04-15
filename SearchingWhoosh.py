from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path

ix = open_dir(r"C:\Users\sebyl\Desktop\Uni\GestioneInfoProg\progettoGestioneInformazione\index")

searcher = ix.searcher()
#print(list(searcher.lexicon("content")))
parser = QueryParser("content", schema=ix.schema)
query = parser.parse("Orwell")
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



