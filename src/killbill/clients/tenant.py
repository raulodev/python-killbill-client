from typing import Union
from killbill.clients.base import BaseClient


class TenantClient(BaseClient):
    """Client for the Kill Bill tenant API"""

    def create(
        self,
        api_key: str,
        api_secret: str,
        created_by: str,
        reason: str = None,
        comment: str = None,
    ) -> Union[str, None]:
        """Creates a new tenant.

        Returns:
            str or None: The tenant's ID or None if the request failed.
        """

        payload = {
            "apiKey": api_key,
            "apiSecret": api_secret,
        }

        response = self._post(
            "tenants",
            payload=payload,
            headers={
                "X-Killbill-CreatedBy": created_by,
                "X-Killbill-Reason": reason,
                "X-Killbill-Comment": comment,
            },
        )

        self._raise_for_status(response)

        return self._get_uuid(response.headers.get("Location"))
