from abc import ABC, abstractmethod
from typing import Tuple, Hashable, List, Any


class Reducer(ABC):

    @staticmethod
    @abstractmethod
    def reduce(self, key: Hashable, values: List[Any]) -> Tuple[Hashable, Any]:
        return key, "some value"
