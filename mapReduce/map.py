from abc import ABC, abstractmethod


class Mapper(ABC):

    @abstractmethod
    def map(self, key: str, value: any) -> tuple:
        pass

