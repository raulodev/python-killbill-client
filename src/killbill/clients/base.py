from urllib.parse import urlparse
import requests
from requests.exceptions import JSONDecodeError
from killbill.exceptions import KillBillError, UnknownError, AuthError, NotFoundError


class BaseClient:
    """Base class for the Kill Bill API client"""

    def __init__(
        self,
        username: str,
        password: str,
        api_url: str = "http://localhost:8080",
        timeout: int = 30,
    ):
        self.api_url = api_url
        self.username = username
        self.password = password
        self.timeout = timeout

    def _post(
        self,
        endpoint: str,
        headers: dict,
        payload: dict = None,
        data=None,
        params: dict = None,
    ):
        """Make a POST request to the Kill Bill API"""

        response = requests.post(
            f"{self.api_url}/1.0/kb/{endpoint}",
            json=payload,
            data=data,
            timeout=self.timeout,
            auth=(self.username, self.password),
            headers=headers,
            params=params,
        )
        return response

    def _delete(
        self,
        endpoint: str,
        headers: dict,
        payload: dict = None,
        data=None,
        params: dict = None,
    ):
        """Make a DELETE request to the Kill Bill API"""

        response = requests.delete(
            f"{self.api_url}/1.0/kb/{endpoint}",
            json=payload,
            data=data,
            timeout=self.timeout,
            auth=(self.username, self.password),
            headers=headers,
            params=params,
        )
        return response

    def _get(
        self,
        endpoint: str,
        headers: dict,
        payload: dict = None,
        params: dict = None,
    ):
        """Make a GET request to the Kill Bill API"""

        response = requests.get(
            f"{self.api_url}/1.0/kb/{endpoint}",
            json=payload,
            timeout=self.timeout,
            auth=(self.username, self.password),
            headers=headers,
            params=params,
        )
        return response

    def _put(
        self,
        endpoint: str,
        headers: dict,
        payload: dict = None,
        data=None,
        params: dict = None,
    ):
        """Make a POST request to the Kill Bill API"""

        response = requests.put(
            f"{self.api_url}/1.0/kb/{endpoint}",
            json=payload,
            data=data,
            timeout=self.timeout,
            auth=(self.username, self.password),
            headers=headers,
            params=params,
        )
        return response

    def _raise_for_status(self, response):
        """Raise an exception if the response status code is not 2xx"""

        status_code = response.status_code

        if status_code >= 400:

            if status_code == 401:
                raise AuthError

            if status_code == 404:
                raise NotFoundError

            # Try get error message from kill bill api
            error_message = None

            try:
                error_message = response.json().get("message")
            except JSONDecodeError:
                error_message = response.text

            if error_message:
                raise KillBillError(error_message)

            raise UnknownError

    def _get_uuid(self, url: str = None):
        """Return uuid from url location"""
        if url:
            return urlparse(url).path.split("/")[-1]
