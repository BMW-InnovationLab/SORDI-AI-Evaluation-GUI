from abc import abstractmethod, ABC, ABCMeta

from domain.models.evaluation_job_results import EvaluationJobResults


class AbstractResultsRepository(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def save_ground_truths(self, uid: str, evaluation_job_results: EvaluationJobResults) -> None:
        pass

    @abstractmethod
    def save_predictions(self, uid: str, evaluation_job_results: EvaluationJobResults) -> None:
        pass

    @abstractmethod
    def get_results(self, uid: str) -> EvaluationJobResults:
        pass

    @abstractmethod
    def delete_results(self, uid: str) -> None:
        pass
