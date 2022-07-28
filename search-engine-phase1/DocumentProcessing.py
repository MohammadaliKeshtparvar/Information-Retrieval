import pickle

import pandas as pd

from Index import Posting
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
            for position, term in enumerate(terms):
                posting = Posting(count, position)
                if term in self.postingLists.keys():
                    self.postingLists.get(term).insertToPostingList(posting)
                else:
                    self.postingLists[term] = PostingList(posting)
            # if count == 10:
            #     f = open("../test.txt", "wb")
            #     pickle.dump(self.postingLists, f)
            #     f.close()
            #     break
        f = open("../inverted-index-without-stopwords.dat", "wb")
        pickle.dump(self.postingLists, f)
        f.close()
