import os
import shutil

from domain.contracts.abstract_error_images_service import AbstractErrorImagesService

class ErrorImagesService(AbstractErrorImagesService):

    def save_error_image(self, image_path:str, output_folder_path:str) -> None:

        error_images_path = os.path.join(output_folder_path, '03-Error Images')

        if not os.path.isdir(error_images_path):
            os.makedirs(error_images_path)

        shutil.copy2(image_path, error_images_path)

