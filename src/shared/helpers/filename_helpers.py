import os
from datetime import datetime

def get_filename_without_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[0]


def get_filename_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[1]


def get_name_with_timestamp(filename:str) -> str:
    now = datetime.now()
    timestamp:str = now.strftime("%Y%m%dT%H%M%S")
    return filename + "_" +timestamp