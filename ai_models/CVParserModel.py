from abc import ABC, abstractmethod

class CVParserModel(ABC):
    @abstractmethod
    def query(self, cv_text):
        pass