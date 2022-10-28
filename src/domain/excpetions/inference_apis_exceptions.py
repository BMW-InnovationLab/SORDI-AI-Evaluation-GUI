from domain.excpetions.application_error import ApplicationError


class InvalidInferenceApiUrl(ApplicationError):

    def __init__(self):
        self.status_code = 502
        self.message = "Invalid url of unreachable inference api"


class ModelsDiscoveryError(ApplicationError):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
