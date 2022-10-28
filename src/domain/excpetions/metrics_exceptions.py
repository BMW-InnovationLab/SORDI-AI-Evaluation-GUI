from domain.excpetions.application_error import ApplicationError


class NoResultsException(ApplicationError):
    def __init__(self):
        self.status_code: int = 400
        self.message: str = "Metric results are not ready yet"
