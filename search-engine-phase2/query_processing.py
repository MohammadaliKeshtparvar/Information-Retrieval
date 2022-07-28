import pickle
import math
from typing import Dict
import re
import time

from PreprocessingUtils import Preprocessing
from Index import PostingListOptimize

preprocessing = Preprocessing()
news_title, news_url = preprocessing.loadResult()
news_content = preprocessing.loadData()
inverted_list_file = "../index/inverted-index-opt-weighted-phase2.dat"
champion_list_file = "../index/inverted-index-opt-weighted-champion-phase2.dat"
# inverted_index: Dict[str, PostingListOptimize] = pickle.load(open(champion_list_file, "rb"))
inverted_index: Dict[str, PostingListOptimize] = pickle.load(open(inverted_list_file, "rb"))
doc_lengths: list = pickle.load(open("../index/doc_lengths-phase2.dat", "rb"))
document_number = len(doc_lengths)


# calculate tf for the term of the query
def calculate_tf(term, query):
    occurrence = query.count(term)
    return 1 + math.log(occurrence, 10)


def calculate_idf(term: str):
    inverted = inverted_index[term]
    number = document_number / inverted.frequency
    return math.log(number, 10)


# extract tokens after normalizing query
def preprocessing_query(query: str) -> list:
    terms = preprocessing.getTokens(query)
    terms = preprocessing.getStems(terms)
    terms = preprocessing.deleteStopWords(terms)
    return terms


def print_result(result: dict, result_size: int, query: list, start_time):
    print(f'{result_size} documents found that have at least 0.0001 consie score with user query')
    print('----------------------------------------')
    print('The results are ranked in the following order')
    print(result)
    print('----------------------------------------')
    count = 0
    for doc_id in result.keys():
        print(f'rank: {count + 1} , doc_id: {doc_id} , score: {result[doc_id]}')
        print(f'title: {news_title[doc_id]}\nURL: {news_url[doc_id]}')
        res_content = []
        for term in query:
            content = re.findall("[.!?].*%s.*[.!?]" % term, news_content[doc_id])
            if content is None or len(content) == 0:
                content = re.findall(".*%s.*" % term, news_content[doc_id])
            res_content.extend(content)
        print(f'content: {res_content}')
        count += 1
        if count == 5:
            break
        print(f'----------------------------------------')
    print("--- response time = %s seconds ---" % (round(time.time() - start_time, 3)))
    print(f'----------------------------------------')


def cosine_score(query: str):
    start_time = time.time()
    score = {}
    terms = preprocessing_query(query)
    for term in terms:
        if term not in inverted_index.keys():
            continue
        for doc in inverted_index[term].docIdWeight.keys():
            w_td = inverted_index[term].docIdWeight[doc]
            w_tq = calculate_idf(term) * calculate_tf(term, terms)
            if doc in score.keys():
                score[doc] = score[doc] + round(w_td * w_tq, 4)
            else:
                score[doc] = round(w_td * w_tq, 4)
    for doc_id in score.keys():
        score[doc_id] = round(score[doc_id] / doc_lengths.__getitem__(doc_id), 4)
    score = {k: v for k, v in sorted(score.items(), key=lambda item: item[1], reverse=True)}
    score = {k: v for k, v in score.items() if v != 0}
    print_result(score, len(score), terms, start_time)
    return score


# cosine_score('فوتبال')
# cosine_score('کارشناس')
# cosine_score('زیمباوه')
# cosine_score('کنگره آمریکا')
# cosine_score('تحریم های آمریکا علیه ایران')
# cosine_score('اورشلیم صهیونیست')
# cosine_score('زیمباوه')
# cosine_score('اقتصاددان غرب')
# cosine_score('لیگ برتر کشتی')
# cosine_score('المپیاد کامپیوتر')
while True:
    user_query = input('query: ')
    cosine_score(user_query)
