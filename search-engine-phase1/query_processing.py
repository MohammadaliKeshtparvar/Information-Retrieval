import pickle
import re
import time

from PreprocessingUtils import Preprocessing

preprocessing = Preprocessing()
news_title, news_url = preprocessing.loadResult()
inverted_index: dict = pickle.load(open("../index/inverted-index.dat", "rb"))


# extract tokens after normalizing query
def preprocessing_query(query: str) -> list:
    terms = preprocessing.getTokens(query)
    terms = preprocessing.getStems(terms)
    terms = preprocessing.deleteStopWords(terms)
    return terms


# remove duplicated token from query after preprocessing
def remove_duplicate(terms: list):
    return list(dict.fromkeys(terms))


# finds their common between the two lists
def merge_doc_id(doc_id_list1, doc_id_list2):
    counter1, counter2 = 0, 0
    size_1, size_2 = len(doc_id_list1), len(doc_id_list2)
    intersect_list = []
    while counter1 != size_1 and counter2 != size_2:
        if doc_id_list1[counter1] == doc_id_list2[counter2]:
            intersect_list.append(doc_id_list1[counter1])
            counter1 += 1
            counter2 += 1
        elif doc_id_list1[counter1] > doc_id_list2[counter2]:
            counter2 += 1
        else:
            counter1 += 1
    return intersect_list


# combines the two lists in ascending order
def combine_list(list1, list2):
    counter_1, counter_2 = 0, 0
    size_1, size_2 = len(list1), len(list2)
    res = []
    while counter_1 < size_1 and counter_2 < size_2:
        if list1[counter_1] < list2[counter_2]:
            res.append(list1[counter_1])
            counter_1 += 1
        else:
            res.append(list2[counter_2])
            counter_2 += 1
    res = res + list1[counter_1:] + list2[counter_2:]
    return res


# counts the number of repetitions in a list
def count_doc_occurrence(doc_id_list):
    result, frequency = {}, 1
    if len(doc_id_list) == 1:
        result[doc_id_list.__getitem__(0)] = 1
        return result
    try:
        for i in range(0, len(doc_id_list) - 1):
            if doc_id_list[i] == doc_id_list[i + 1]:
                frequency += 1
            else:
                result[doc_id_list[i]] = frequency
                frequency = 1
        if doc_id_list[-1] != doc_id_list[-2]:
            result[doc_id_list[-1]] = 1
            return result
        else:
            return result
    except IndexError:
        return result


def reverse_dic(result: dict) -> dict:
    split_result = {}
    for k, v in result.items():
        if v in split_result.keys():
            split_result[v].append(k)
        else:
            split_result[v] = [k]
    split_result = {k: v for k, v in sorted(split_result.items(), key=lambda item: item[0], reverse=True)}
    return split_result


# sorts by frequency of tokens in document
def document_ranking(doc_occurrence, phrase_res, terms, term_size):
    result = {}
    for i in range(0, term_size):
        try:
            doc_id = doc_occurrence[term_size - i]
            frequency_list = []
            for j in doc_id:
                frequency = 0
                for term in terms:
                    try:
                        frequency += inverted_index[term].frequencyInDoc[j]
                    except KeyError:
                        frequency += 0
                if j in phrase_res.keys():
                    frequency += len(phrase_res[j])
                frequency_list.append(frequency)
        except KeyError:
            continue
        res_1 = {doc_id[k]: frequency_list[k] for k in range(len(doc_id))}
        var_1 = {k: v for k, v in sorted(res_1.items(), key=lambda item: item[1], reverse=True)}
        result[term_size - i] = var_1
    return result


# executes simple query
def simple_query(terms: list) -> dict:
    terms = remove_duplicate(terms)
    res = []
    if len(terms) == 1:
        try:
            res = list(inverted_index[terms.__getitem__(0)].docIdPositionList.keys())
        except KeyError:
            print(f'{terms[0]} does not exist in the dictionary')
    for i in range(0, len(terms) - 1):
        if i == 0:
            try:
                l1 = list(inverted_index[terms.__getitem__(i)].docIdPositionList.keys())
            except KeyError:
                l1 = []
            try:
                l2 = list(inverted_index[terms.__getitem__(i + 1)].docIdPositionList.keys())
            except KeyError:
                l2 = []
            res = combine_list(l1, l2)
        else:
            try:
                l1 = list(inverted_index[terms.__getitem__(i + 1)].docIdPositionList.keys())
            except KeyError:
                l1 = []
            res = combine_list(res, l1)
    var = count_doc_occurrence(res)
    return var


def execute_not_query(terms: list) -> list:
    res = []
    if len(terms) == 1:
        res = list(inverted_index[terms.__getitem__(0)].docIdPositionList.keys())
    for i in range(0, len(terms) - 1):
        if i == 0:
            res = combine_list(list(inverted_index[terms.__getitem__(i)].docIdPositionList.keys())
                               , list(inverted_index[terms.__getitem__(i + 1)].docIdPositionList.keys()))
        else:
            res = combine_list(res, list(inverted_index[terms.__getitem__(i + 1)].docIdPositionList.keys()))
    return remove_duplicate(res)


def execute_phrasal_query(query: str):
    terms = preprocessing_query(query)
    terms = remove_duplicate(terms)
    res = []
    try:
        if len(terms) == 1:
            res = list(inverted_index[terms.__getitem__(0)].docIdPositionList.keys())
        for i in range(0, len(terms) - 1):
            if i == 0:
                res = merge_doc_id(list(inverted_index[terms.__getitem__(i)].docIdPositionList.keys())
                                   , list(inverted_index[terms.__getitem__(i + 1)].docIdPositionList.keys()))
            else:
                res = merge_doc_id(res, list(inverted_index[terms.__getitem__(i + 1)].docIdPositionList.keys()))
        result = find_phrase_with_position(res, terms)
        print(f'phrase result = {result}')
        return result
    except KeyError:
        return {}


def find_phrase_with_position(common_doc_id: list, terms: list) -> dict:
    result = {}
    for doc_id in common_doc_id:
        seq = find_sequence_position(inverted_index[terms[0]].docIdPositionList[doc_id],
                                     inverted_index[terms[1]].docIdPositionList[doc_id])
        seq_size = len(seq)
        if seq_size == 0:
            continue
        seq_list = []
        for s in range(0, seq_size):
            sequence = [seq[s] - 1, seq[s]]
            for i in range(2, len(terms)):
                next_num = seq[s] + i - 1
                if next_num in inverted_index[terms[i]].docIdPositionList[doc_id]:
                    sequence.append(next_num)
                else:
                    break
            if len(sequence) == len(terms):
                seq_list.append(sequence)
        if len(seq_list) > 0:
            result[doc_id] = seq_list
    return result


# finds sequence in two lists
def find_sequence_position(position_list_1: list, position_list_2: list) -> list:
    index1, index2 = 0, 0
    size_1, size_2 = len(position_list_1), len(position_list_2)
    result = []
    while index1 < size_1 and index2 < size_2:
        if position_list_1[index1] - position_list_2[index2] == -1:
            result.append(position_list_2[index2])
            index1 += 1
            index2 += 1
        elif position_list_1[index1] < position_list_2[index2]:
            index1 += 1
        else:
            index2 += 1
    return result


def find_not_query(terms: list) -> list:
    not_query_terms = []
    for count, t in enumerate(terms):
        if bool(re.search('!$', t)):
            try:
                terms[count] = t.replace('!', '')
                not_query_terms.append(terms[count + 1])
            except IndexError:
                break
    return not_query_terms


def print_result(result: dict, result_size: int):
    print(f'{result_size} documents found that have at least 1 word of user query')
    print('----------------------------------------')
    print('The results are ranked in the following order')
    print(result)
    print('----------------------------------------')
    count = 0
    for k in result.keys():
        if count == 5:
            break
        for doc_id in result[k].keys():
            print(f'rank: {count + 1} , doc_id: {doc_id} , frequency: {result[k][doc_id]}')
            print(f'title: {news_title[doc_id]}\nURL: {news_url[doc_id]}')
            print(f'----------------------------------------')
            count += 1
            if count == 5:
                break


def merge_result(simple_res: dict, phrase_res: dict):
    for k in phrase_res.keys():
        if k in simple_res.keys():
            simple_res[k] = simple_res[k] + len(phrase_res[k])
        else:
            simple_res[k] = len(phrase_res[k])


def check_query_type(query):
    phrase_query = re.findall('"([^"]*)"', query)
    phrase_result = {}
    for phrase in phrase_query:
        phrase_result.update(execute_phrasal_query(phrase))
    query = re.sub('"([^"]*)"', '', query)
    terms = preprocessing_query(query)
    not_query_terms = find_not_query(terms)
    simple_query_terms = [x for x in terms if x not in not_query_terms]
    simple_query_terms = remove_duplicate(simple_query_terms)
    not_query_terms = remove_duplicate(not_query_terms)
    not_query_res = execute_not_query(not_query_terms)
    simple_query_res = simple_query(simple_query_terms)
    merge_result(simple_query_res, phrase_result)
    try:
        result = {k: v for k, v in simple_query_res.items() if k not in not_query_res}
    except AttributeError:
        result = {}
    result_size = len(result)
    result = reverse_dic(result)
    var = document_ranking(result, phrase_result, simple_query_terms, len(phrase_query) + len(simple_query_terms))
    print_result(var, result_size)


while True:
    user_query = input('query : ')
    start_time = time.time()
    check_query_type(user_query)
    print("--- %s seconds ---" % (time.time() - start_time))

# check_query_type("امریکا ! فوتبال کشتی")
# check_query_type("ایران ! فوتبال امریکا !")
# check_query_type('امریکا انگلیس "گروه سوم جام جهانی" افریقا')
# check_query_type('تحریم های امریکا علیه ایران')
# check_query_type('تحریم های امریکا ! ایران')
# check_query_type('امریکا')
# check_query_type('"کنگره ضدتروریست"')
# check_query_type('"کنگره ضدتروریست" فوتبال')
# check_query_type(' "تحریم هسته ای" امریکا ! ایران')
# check_query_type('اورشلیم ! صهیونیست')
# check_query_type('"تحریم های هسته ای"')
# check_query_type('زیمباوه')
