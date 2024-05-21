from abc import ABC, abstractmethod

class JobChatBotModel(ABC):
    @abstractmethod
    def attachJob(self, job_text, topic):
        pass
    
    @abstractmethod
    def attachCV(self, cv_text):
        pass
    
    @abstractmethod
    def query(self, message):
        pass