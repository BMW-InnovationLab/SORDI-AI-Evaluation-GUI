from abc import ABC, ABCMeta, abstractmethod

class AbstractErrorImagesService(ABC):

    __metaclass__  = ABCMeta

    @abstractmethod
    def save_error_image(self, image_path:str, output_folder_path:str) -> None:
        pass
