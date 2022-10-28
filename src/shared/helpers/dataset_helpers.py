import os


def get_dataset_path(dataset_name: str, job_type: str) -> str:
    return os.path.join('../datasets/', job_type, dataset_name)
