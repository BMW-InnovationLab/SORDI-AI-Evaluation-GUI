import os
import shutil

from domain.contracts.abstract_dataset_validaton_service import AbstractDatasetValidationService
from domain.excpetions.validation_exceptions import InvalidDataset
from domain.models.dataset_information import DatasetInformation
from domain.models.dataset_parameters import DatasetParameters
from domain.models.inference_types import InferenceTypes
from shared.helpers.archive_helpers import extract_archive
from shared.helpers.dataset_helpers import get_dataset_path
from shared.helpers.filename_helpers import get_filename_without_extension, get_filename_extension, \
    get_name_with_timestamp


class DatasetArchiveExtractionService:
    def __init__(self, dataset_validator: AbstractDatasetValidationService):
        self._dataset_validator_service = dataset_validator

    def extract_dataset_archive(self, filename: str, file_content) -> DatasetInformation:
        dataset = self._extract_dataset_archive(filename, file_content)
        dataset_parameters_test: DatasetParameters = DatasetParameters(dataset_name=dataset,
                                                                       job_type='image_classification')
        if self._validate_type(dataset_parameters_test):
            return DatasetInformation(name=dataset, type=InferenceTypes.image_classification)

        dataset_parameters_test.job_type = 'object_detection'

        if self._validate_type(dataset_parameters_test):
            return DatasetInformation(name=dataset, type=InferenceTypes.object_detection)

        os.remove(os.path.join('../datasets', dataset))
        raise InvalidDataset

    def _validate_type(self, dataset_parameters: DatasetParameters) -> bool:
        root_path: str = os.path.join("../datasets", dataset_parameters.dataset_name)
        type_path: str = get_dataset_path(dataset_parameters.dataset_name, dataset_parameters.job_type)
        shutil.move(root_path, type_path)
        type_valid = self._dataset_validator_service.check_dataset_valid(dataset_parameters)
        if not type_valid:
            shutil.move(type_path, root_path)
        return type_valid

    def _extract_dataset_archive(self, filename: str, file_content) -> str:
        datasets_folder: str = "../datasets"

        basename: str = get_filename_without_extension(filename)
        basename = get_name_with_timestamp(basename)
        extension = get_filename_extension(filename)
        upload_filename = basename + "." + extension

        upload_folder: str = os.path.join(datasets_folder, basename)
        upload_path: str = os.path.join(datasets_folder, upload_filename)

        with open(upload_path, 'ab') as f:
            for chunk in iter(lambda: file_content.read(100000), b''):
                f.write(chunk)

        try:
            extract_archive(upload_path, upload_folder)
            os.remove(upload_path)

            for element in os.listdir(upload_folder):

                element_path: str = os.path.join(upload_folder, element)

                if os.path.isdir(element_path):
                    for f in os.listdir(element_path):
                        shutil.move(os.path.join(element_path, f), upload_folder)

                shutil.rmtree(element_path)

            return basename

        except:
            os.remove(upload_path)
            raise Exception
