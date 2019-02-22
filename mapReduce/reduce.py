from abc import ABC, abstractmethod


class Reducer(ABC):

    @abstractmethod
    def reduce(self, key: str, values: list) -> tuple:
        pass
