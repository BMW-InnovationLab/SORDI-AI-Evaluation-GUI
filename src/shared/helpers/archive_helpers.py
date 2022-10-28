import os
from zipfile import ZipFile


def extract_archive(archive_to_extract, output_path:str) -> None:
    with ZipFile(archive_to_extract, 'r') as zipObj:
        zipObj.extractall(output_path)




def create_archive(folder_to_compress:str, archive_name:str, output_folder:str) -> None:
    archive_name = archive_name+".zip"
    
    archive_path = os.path.join(output_folder, archive_name)

    file_paths = []

    for root, directories, files in os.walk(folder_to_compress):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    

    with ZipFile(archive_path, 'w') as zip:
        for f in file_paths:
            path = f.split("/")[2:]
            path = "/".join(path)
            zip.write(f, arcname=path)