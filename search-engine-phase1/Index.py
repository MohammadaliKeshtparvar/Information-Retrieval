from typing import Dict, List


class Posting:
    def __init__(self, docId, pos):
        self.docId: int = docId
        self.position = [pos]
        self.frequency = 1

    def insertPosition(self, position):
        self.frequency += 1
        self.position.append(position)


class PostingList:
    def __init__(self, posting: Posting):
        self.docIdPositionList: Dict[int, List[int]] = {posting.docId: posting.position}
        self.frequencyInDoc: Dict[int, int] = {posting.docId: 1}
        # self.frequency = 1
        self.allFrequency = 1

    def __insertPosting(self, posting: Posting):
        # self.frequency += 1
        self.allFrequency += 1
        self.docIdPositionList[posting.docId] = posting.position
        self.frequencyInDoc[posting.docId] = 1

    def __insertPosition(self, docId, position):
        self.allFrequency += 1
        self.docIdPositionList.get(docId).append(position)
        self.frequencyInDoc[docId] = 1 + self.frequencyInDoc.get(docId)

    def insertToPostingList(self, posting: Posting):
        if posting.docId in self.docIdPositionList.keys():
            self.__insertPosition(posting.docId, posting.position.__getitem__(0))
        else:
            self.__insertPosting(posting)
