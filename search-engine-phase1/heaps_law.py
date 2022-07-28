import math
import matplotlib.pyplot as plt
from PreprocessingUtils import Preprocessing
from scipy.optimize import curve_fit
import numpy as np

preprocessing = Preprocessing()
tokens = list()
vocabularies = set()
token_list = list()
vocabularies_list = list()
news_content = preprocessing.loadData()
real_result_dic = {}
all_doc = len(news_content)


def func(x_, a_, b_):
    return a_ * x_ + b_


def counter_token_and_vocab():
    for count, nc in enumerate(news_content):
        print(f'docId : {count}')
        terms = preprocessing.getTokens(nc)
        terms = preprocessing.deleteStopWords(terms)
        terms = preprocessing.getStems(terms)
        tokens.extend(terms)
        vocabularies.update(terms)
        token_list.append(math.log10(len(tokens)))
        vocabularies_list.append(math.log10(len(vocabularies)))
        if count + 1 in [500, 1000, 1500, 2000, all_doc]:
            real_result_dic[count + 1] = {'all_tokens': len(tokens), 'vocab': len(vocabularies)}


def print_info():
    print('\n---------------------with stemming---------------------')
    print(f'log M = {b} * log T + {log_k}')
    print(f'b = {b} , k = {k}')
    print('----------------------------------------')
    print(f'real result    {real_result_dic}\n----------------------------------------')
    print(f'expected result{expected_result_dic}\n----------------------------------------')


counter_token_and_vocab()
expected_result_dic = real_result_dic.copy()
popt, _ = curve_fit(func, token_list, vocabularies_list)
b, log_k = popt
b = float(format(b, ".5f"))
k = pow(10, float(format(log_k, ".5f")))
x = np.linspace(1.8, 7, 100)
y = b * x + log_k
plt.plot(x, y, '--')
for doc_num in [500, 1000, 1500, 2000, all_doc]:
    T = expected_result_dic[doc_num]['all_tokens']
    m = int(k * math.pow(T, b))
    expected_result_dic[doc_num] = {'all_tokens': T, 'vocab': m}

print_info()
plt.plot(token_list, vocabularies_list)
plt.legend(["expected", "real"])
plt.title('with stemming')
plt.xlabel("log10 T")
plt.ylabel("log10 M")
plt.show()
