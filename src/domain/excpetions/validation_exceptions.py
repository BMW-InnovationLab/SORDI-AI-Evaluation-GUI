from domain.excpetions.application_error import ApplicationError


class InvalidInferenceApiType(ApplicationError):

    def __init__(self):
        self.status_code = 422
        self.message = "Invalid inference api type"


class InvalidDataset(ApplicationError):
    def __init__(self):
        self.status_code = 422
        self.message = "Invalid dataset"


class InvalidModel(ApplicationError):
    def __init__(self):
        self.status_code = 422
        self.message = "Invalid model"

class InvalidLabelsFormat(ApplicationError):
    def __init__(self):
        self.status_code = 422
        self.message = "Invalid Labels Format"
        super().__init__(self.message)
class InvalidJobId(ApplicationError):
    def __init__(self):
        self.status_code = 422
        self.message = "Invalid Job Id"


class InvalidBatchSize(ApplicationError):
    def __init__(self):
        self.status_code = 422
        self.message = "Invalid Batch Size"
class EmptyDataset(ApplicationError):
    def __init__(self):
        self.status_code = 422
        self.message = "Invalid Dataset: Dataset empty or not valid"
        super().__init__(self.message)


class EmptyLinkages(ApplicationError):
    def __init__(self):
        self.status_code = 400
        self.message = "Linkages is empty"
        super().__init__(self.message)