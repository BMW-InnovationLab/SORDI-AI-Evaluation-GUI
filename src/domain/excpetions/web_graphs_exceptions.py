from domain.excpetions.application_error import ApplicationError


class InvalidLabelName(ApplicationError):
    def __init__(self):
        self.status_code: int = 400
        self.message: str = "Invalid Label Name"


class WebGraphsGenralException(ApplicationError):
    def __init__(self, message: str):
        self.status_code: int = 500
        self.message: str = message
