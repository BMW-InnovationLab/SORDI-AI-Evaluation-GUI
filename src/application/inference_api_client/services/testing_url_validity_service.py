import requests
import os

from domain.contracts.abstract_testing_url_validity_service import AbstractTestingUrlValidityService


class TestingUrlValidityService(AbstractTestingUrlValidityService):

    def test_url_validity(self, url: str) -> bool:
        try:
            url = os.path.join(url, 'docs')
            response = requests.get(url,timeout=30)
            return True if response.status_code == 200 else False
        except:
            return False

