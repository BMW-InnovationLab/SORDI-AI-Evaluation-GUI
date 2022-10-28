from enum import Enum


class OutputImagesTypes(Enum):
    image_classification: str = "image_classification"
    object_detection: str = "object_detection"
