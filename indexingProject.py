import nltk
from nltk.corpus import stopwords
from whoosh.index import create_in
from whoosh.fields import *
import os, os.path

dir_path = r'C:\Users\sebyl\Desktop\Uni\GestioneInfoProg\FILES'
# Defines the way the file is written
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), author=ID(stored=True), content=TEXT(analyzer=analysis.StemmingAnalyzer()))

ix = create_in(r"C:\Users\sebyl\Desktop\Uni\GestioneInfoProg\index", schema)
writer = ix.writer()

# list to store files
res = []

# usefull variables
i = 0
limit = 50000

# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        res.append(path)
        i += 1
    # upper limit for number of files
    if i >= limit:
        break

for file in res: 
    fpath = str(dir_path + '\\' + file)
    with open(fpath, 'r', encoding='utf-8') as fd:
        title = fd.readline()
        aut = fd.readline()
        content = fd.read()
        writer.add_document(title=title, path=fpath, author=aut, content=content)

writer.commit()