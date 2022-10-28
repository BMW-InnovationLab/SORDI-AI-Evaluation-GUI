from abc import ABC, ABCMeta, abstractmethod

class AbstractDatasetArchiveExtractionService(ABC):

    __metaclass__ = ABCMeta

    @abstractmethod
    def extract_dataset_archive(self, filename:str, file_content) -> str:
        pass