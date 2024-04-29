import nltk
from nltk.corpus import stopwords
from whoosh.index import create_in
from whoosh.fields import *
import os, os.path
from transformers import AutoModelForSequenceClassification, AutoConfig
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax

dir_path = r'C:\Users\sebyl\Desktop\Uni\GestioneInfoProg\FILES'

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
max_length = 1024


# Defines the way the file is written
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), author=TEXT(stored=True, analyzer=None), review=TEXT(analyzer=analysis.StemmingAnalyzer()), sentimentType=KEYWORD(stored=True), sentimentValue=NUMERIC)

ix = create_in(r"C:\Users\sebyl\Desktop\Uni\GestioneInfoProg\progettoGestioneInformazione\index", schema)
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
    with open(os.path.join(dir_path, file), 'r', encoding='utf-8') as fd:
    #fpath = str(dir_path + '\\' + file)
        #with open(fpath, 'r', encoding='utf-8') as fd:
        title = fd.readline()
        aut = fd.readline().replace("[", "").replace("]", "").replace("'", "").replace("\n", "").replace("nan", "")
        review = fd.read()

        encoded_input = tokenizer(review, max_length=max_length, return_tensors='pt', truncation=True)

        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        tmp_dict = {
            'negative': scores[0],
            'neutral': scores[1],
            'positive': scores[2]
        }

        #print(tmp_dict)

        max_score = max(tmp_dict.values())
        max_type = list(tmp_dict.keys())[list(tmp_dict.values()).index(max_score)]

        #print(f'Sentiment: {max_type}, {max_score}')

        writer.add_document(title=title, path=os.path.join(dir_path, file), author=aut, review=review, sentimentType=max_type, sentimentValue=max_score)

writer.commit()