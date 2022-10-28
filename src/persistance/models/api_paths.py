import os

from pydantic import BaseModel, validator


class ApiPaths(BaseModel):
    base_dataset: str
    object_detection_datasets: str
    classification_datasets: str
    inference_api_services: str
    # models: str

    @validator('object_detection_datasets', 'classification_datasets')
    def is_dir(cls, value):
        assert os.path.isdir(value), "{} should be a directory".format(value)
        return value

    # @validator('inference_api_services')
    # def is_file(cls, value):
    #     assert os.path.isfile(value), "{} should be a file".format(value)
    #     return value
