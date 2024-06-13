# progettoGestioneInformazione

Gruppo: Alberini Mattia, Allagui Nassim, Lupu Sebastian

Abbiamo realizzato 4 versioni di serch-engine che offrono funzioni diverse e utilizzano differenti modelli di ranking
- Base search engine, che permette di utilizzare i classici modelli di ranking. 
- Manual sentiment search engine, integra un modello di ranking che sfrutta il valore di sentiment dei file; si chiama "manual sentiment" perché in questo modello il sentimento non viene deciso in maniera trasparente ma viene richiesto all'utente. 
- Automatic sentiment search engine, integra un modello di ranking che sfrutta il valore di sentiment dei file; si chiama "Auto sentiment" perché in questo modello il sentimento viene ricavato dalla interrogazione dell'utente in maniera trasparente.
- Word2vec search engine, integra un modello di ranking che sfrutta un modello di word2vec ricavato con CBOW. 

FUNZIONAMENTO: 
Il file searchingWhoosh implementa il sistema di ricerca che permette di eseguire ricerce nei vari campi dello schema definito. 
Tipologie di ricerca: 
- Titolo
- Autore
- Genere
- Particolari nella recensione

Le query eseguite possono essere ad esempio: 
- Full-text search: word1 word2
- Phrasal search: "word1 word2"
- Wildcard search: word*

Abbiamo fornito la possibilità di scegliere tra i vari modelli di ranking, tra cui quelli di defaul e quelli generati da noi: 
- BM25F
- TF_IDF
- Frequency
- BM25F + Sentiment analysis
- BM25F + word2vec similarity

MODULI
- progGI.py: file che analizza il dataset csv e genera il pool di file. 
- indexingProject.py: file per la generazione dell inverted index con whoosh, dove viene definito lo schema e valutata inoltre la sentiment dei singoli file. 
- SearchingWhoosh: file che gestisce il sistema di ricerca attraverso le scelte presentate con una semplice interfaccia
- word2vec/generate_w2v_model.py: file per la generazione del modello di word2vec con gensim 
- word2vec/generate_index_w2v.py: file per la generazione di un secondo inverted index, che per questioni implementative gestisce solo le query con word2vec
- word2vec/queryw2v.py: file per la gestione delle interrogazioni sull'index che gestisce il word2vec.


