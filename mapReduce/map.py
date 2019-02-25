from abc import ABC, abstractmethod
from typing import Tuple, Hashable, Any


class Mapper(ABC):

    @staticmethod
    @abstractmethod
    def map(key: Hashable, value: Any) -> Tuple[Hashable, Any]:
        return key, value
