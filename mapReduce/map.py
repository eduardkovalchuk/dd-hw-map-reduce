from abc import ABC, abstractmethod
from typing import Tuple, Hashable, Any


class Mapper(ABC):

    @abstractmethod
    def map(self, key: Hashable, value: Any) -> Tuple[Hashable, Any]:
        pass

