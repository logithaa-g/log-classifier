from abc import ABC, abstractmethod

class BaseClassifier(ABC):

    @abstractmethod
    def match(self, event):
        pass