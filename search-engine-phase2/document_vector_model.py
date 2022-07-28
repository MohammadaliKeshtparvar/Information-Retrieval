import pickle
import math
import pandas as pd
from typing import Dict

from PreprocessingUtils import Preprocessing
from Index import PostingList
from Index import PostingListOptimize

preprocessing = Preprocessing()
inverted_index: Dict[str, PostingList] = pickle.load(open("../index/inverted-index-phase2.dat", "rb"))
news_content: pd.DataFrame = preprocessing.loadData()
document_number = len(news_content)
doc_lengths = []
inverted_index_weight = {}


def calculate_tf(token, doc_id):
    inverted = inverted_index[token]
    frequency_in_doc = inverted.frequencyInDoc[doc_id]
    return 1 + math.log(frequency_in_doc, 10)


def calculate_idf(token):
    inverted = inverted_index[token]
    number = document_number / inverted.frequency
    return math.log(number, 10)


for count, nc in enumerate(news_content):
    terms = preprocessing.getTokens(nc)
    terms = preprocessing.deleteStopWords(terms)
    terms = preprocessing.getStems(terms)
    weight_length = 0
    for term in terms:
        if term in inverted_index.keys():
            weight = round(calculate_idf(token=term) * calculate_tf(token=term, doc_id=count), 4)
            weight_length += weight ** 2
            if term in inverted_index_weight.keys():
                inverted_index_weight[term].insertDocId(count, weight)
            else:
                inverted_index_weight[term] = PostingListOptimize(count, weight)
    weight_length = round(weight_length ** 0.5, 4)
    doc_lengths.append(weight_length)
    print(f'docId : {count} | docLengths : {weight_length}')


f1 = open("../index/inverted-index-opt-weighted-phase2.dat", "wb")
pickle.dump(inverted_index_weight, f1)
f1.close()

f2 = open("../index/doc_lengths-phase2.dat", "wb")
pickle.dump(doc_lengths, f2)
f2.close()
