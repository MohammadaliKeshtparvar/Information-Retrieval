from typing import Dict


class PostingList:
    def __init__(self, docId):
        self.docIdWeight: Dict[int, float] = {docId: 0}
        self.frequencyInDoc: Dict[int, int] = {docId: 1}
        self.frequency = 1
        self.allFrequency = 1

    def __insertDocId(self, docId: int):
        self.docIdWeight[docId] = 0
        self.frequency += 1
        self.allFrequency += 1
        self.frequencyInDoc[docId] = 1

    def __increaseFrequencyInDoc(self, docId: int):
        self.allFrequency += 1
        self.frequencyInDoc[docId] = 1 + self.frequencyInDoc.get(docId)

    def insertToPostingList(self, docId: int):
        if docId in self.docIdWeight.keys():
            self.__increaseFrequencyInDoc(docId)
        else:
            self.__insertDocId(docId)


class PostingListOptimize:
    def __init__(self, docId, weight):
        self.docIdWeight: Dict[int, float] = {docId: weight}
        self.frequency = 1

    def insertDocId(self, docId: int, weight: float):
        if docId not in self.docIdWeight.keys():
            self.frequency += 1
        self.docIdWeight[docId] = weight
