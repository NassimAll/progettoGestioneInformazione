from whoosh.index import create_in
from whoosh.fields import *
import os, os.path
from transformers import AutoModelForSequenceClassification, AutoConfig
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax

dir_path = r'C:\Users\sebyl\Desktop\Uni\GestioneInfoProg\FILES'
index_dir = r"C:\Users\sebyl\Desktop\Uni\GestioneInfoProg\progettoGestioneInformazione\index"

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
max_length = 512


# Defines the way the file is written
schema = Schema(title=TEXT(stored=True, analyzer=None), path=ID(stored=True, analyzer=None), author=TEXT(analyzer=None), genre=TEXT(analyzer=None), review=TEXT(analyzer=analysis.StemmingAnalyzer()), positive=NUMERIC(float, stored=True), neutral=NUMERIC(float, stored=True), negative=NUMERIC(float, stored=True))

ix = create_in(index_dir, schema)
writer = ix.writer()

# list to store files
res = []

# usefull variables
i = 0
limit = 50000

for file in os.listdir(dir_path): 
    with open(os.path.join(dir_path, file), 'r', encoding='utf-8') as fd:
        i += 1
        title = fd.readline()
        aut = fd.readline().replace("[", "").replace("]", "").replace("'", "").replace("\n", "").replace("nan", "")
        genre = fd.readline().replace("[", "").replace("]", "").replace("'", "").replace("\n", "").replace("nan", "")
        review = fd.read()

        encoded_input = tokenizer(review, max_length=max_length, return_tensors='pt', truncation=True)

        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        vals_dict = {
            'negative': scores[0],
            'neutral': scores[1],
            'positive': scores[2]
        }

        #print(vals_dict)
        print(i)

        writer.add_document(title=title, path=os.path.join(dir_path, file), author=aut, genre=genre, review=review, positive=scores[2], neutral=scores[1], negative=scores[0])
        if i >= limit:  break


        

writer.commit()