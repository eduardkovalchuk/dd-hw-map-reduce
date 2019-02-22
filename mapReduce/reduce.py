from abc import ABC, abstractmethod
from typing import Tuple, Hashable, List, Any


class Reducer(ABC):

    @abstractmethod
    def reduce(self, key: Hashable, values: List[Any]) -> Tuple[Hashable, Any]:
        pass
