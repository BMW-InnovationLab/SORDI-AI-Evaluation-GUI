from abc import abstractmethod, ABC, ABCMeta


from typing import List


class AbstractTestingUrlValidityService(ABC):

    __metaclass__ = ABCMeta

    @abstractmethod
    def test_url_validity(self, url: str) -> bool:
        pass

