import pickle
from typing import Dict
import itertools

from Index import PostingListOptimize
from PreprocessingUtils import Preprocessing

preprocessing = Preprocessing()
f = "../index/inverted-index-opt-weighted-phase2.dat"
inverted_index: Dict[str, PostingListOptimize] = pickle.load(open(f, "rb"))
doc_lengths: list = pickle.load(open("../index/doc_lengths-phase2.dat", "rb"))
champion_inverted_index = {}

for term in inverted_index.keys():
    top_doc_id = {k: v for k, v in sorted(inverted_index[term].docIdWeight.items()
                                          , key=lambda item: item[1] / doc_lengths[item[0]], reverse=True)}
    top_doc_id = dict(itertools.islice(top_doc_id.items(), 500))
    inverted_index[term].docIdWeight = top_doc_id

f = open("../index/inverted-index-opt-weighted-champion-phase2.dat", "wb")
pickle.dump(inverted_index, f)
f.close()
