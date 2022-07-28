import pickle

import pandas as pd

from Index import PostingList
from PreprocessingUtils import Preprocessing


class DocumentProcessing:

    def __init__(self):
        self.preprocessing = Preprocessing()
        self.postingLists = {}

    def createInvertedIndex(self):
        news_content: pd.DataFrame = self.preprocessing.loadData()
        for count, nc in enumerate(news_content):
            print(f'docId : {count}')
            terms = self.preprocessing.getTokens(nc)
            terms = self.preprocessing.deleteStopWords(terms)
            terms = self.preprocessing.getStems(terms)
            for term in terms:
                if term in self.postingLists.keys():
                    self.postingLists.get(term).insertToPostingList(count)
                else:
                    self.postingLists[term] = PostingList(count)
        f = open("../index/inverted-index-phase2.dat", "wb")
        pickle.dump(self.postingLists, f)
        f.close()
