from abc import ABC, abstractmethod



class InitialConditions_base(ABC):
    @abstractmethod
    def __init__(self, Param):
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def format(self):
        pass

    @abstractmethod
    def save(self):
        pass
