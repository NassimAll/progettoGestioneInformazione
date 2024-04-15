from pandas import *
import itertools 


data = read_csv(r'C:\Users\sebyl\Desktop\GestioneInfoProg\Books_rating.csv\Books_rating.csv')
databooks = read_csv(r'C:\Users\sebyl\Desktop\GestioneInfoProg\books_data.csv\books_data.csv')

author = databooks['authors'].tolist()
categories = databooks['categories'].tolist()

#converting column data to list
title = data['Title'].tolist()
review = data['review/text'].tolist()

c = 0
res = {}
for key in title:
    for value in review:
        res[key] = value
        review.remove(value)
        break
    #c += 1
    #if c == 100: break
#else: c = 0

#print(len(res))
#print(len(author))
#print(len(categories))

b = 1
for (key, aut, cat) in zip(res, author, categories): 
    file = r'C:\Users\sebyl\Desktop\GestioneInfoProg\FILES\\' + 'Book' + str(b) + '.txt'
    b += 1
    
    with open(str(file), 'w', encoding="utf-8") as fd:
        fd.write(str(key))
        fd.write("\n")
        fd.write(str(aut))
        fd.write("\n")
        fd.write(str(cat))
        fd.write("\n")
        fd.write(res[key])
        fd.write("\n")
    