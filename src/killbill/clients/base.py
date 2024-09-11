from urllib.parse import urlparse
import requests
from killbill.errors import KillBillException


class BaseClient:
    """Base class for the Kill Bill API client"""

    def __init__(
        self, username: str, password: str, api_url: str = "http://localhost:8080"
    ):
        self.api_url = api_url
        self.username = username
        self.password = password

    def _post(
        self,
        endpoint: str,
        headers: dict,
        payload: dict = None,
        data=None,
        timeout: int = 1000,
        params: dict = None,
    ):
        """Make a POST request to the Kill Bill API"""

        response = requests.post(
            f"{self.api_url}/1.0/kb/{endpoint}",
            json=payload,
            data=data,
            timeout=timeout,
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
        timeout: int = 1000,
        params: dict = None,
    ):
        """Make a DELETE request to the Kill Bill API"""

        response = requests.delete(
            f"{self.api_url}/1.0/kb/{endpoint}",
            json=payload,
            data=data,
            timeout=timeout,
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
        timeout: int = 1000,
        params: dict = None,
    ):
        """Make a GET request to the Kill Bill API"""

        response = requests.get(
            f"{self.api_url}/1.0/kb/{endpoint}",
            json=payload,
            timeout=timeout,
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
        timeout: int = 1000,
        params: dict = None,
    ):
        """Make a POST request to the Kill Bill API"""

        response = requests.put(
            f"{self.api_url}/1.0/kb/{endpoint}",
            json=payload,
            data=data,
            timeout=timeout,
            auth=(self.username, self.password),
            headers=headers,
            params=params,
        )
        return response

    def _raise_for_status(self, response):
        """Raise an exception if the response status code is not 2xx"""

        if response.status_code == 500:
            raise KillBillException("Internal Server Error")

        if response.status_code == 415:
            raise KillBillException(
                "Unsupported Media Type .The origin server is "
                "refusing to service the request because the payload "
                "is in a format not supported by this method on the target "
                "resource"
            )

        if response.status_code == 404:
            raise KillBillException("Not Found")

        if response.status_code in (401, 405):
            raise KillBillException(response.text)

        if response.status_code >= 400:
            message = response.json().get("message")
            raise KillBillException(message)

    def _get_uuid(self, url: str = None):
        """Return uuid from url location"""
        if url:
            return urlparse(url).path.split("/")[-1]
