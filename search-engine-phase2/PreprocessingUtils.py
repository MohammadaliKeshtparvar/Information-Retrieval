from typing import Tuple

import pandas as pd
from hazm import Normalizer
from hazm import stopwords_list
from parsivar import FindStems
from parsivar import Tokenizer


class Preprocessing:

    def __init__(self):
        self.__tokenizer = Tokenizer()
        self.__normalizer = Normalizer()
        self.__stemmer = FindStems()
        self.__stopWords = stopwords_list()

    # normalizes text before extracting tokens
    def getTokens(self, text: str):
        return self.__tokenizer.tokenize_words(self.normalize(text))

    def normalize(self, text):
        return self.__normalizer.normalize(text)

    def getStems(self, words):
        return [self.__stemmer.convert_to_stem(word) for word in words]

    def deleteStopWords(self, words):
        return [word for word in words if word not in self.__stopWords]

    @staticmethod
    def loadData() -> pd.DataFrame:
        data_frame = pd.read_json('../IR_data_news_12k.json')
        return data_frame.T['content']

    @staticmethod
    def loadResult() -> Tuple[pd.DataFrame, pd.DataFrame]:
        data_frame = pd.read_json('../IR_data_news_12k.json')
        return data_frame.T['title'], data_frame.T['url']
