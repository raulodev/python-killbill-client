from killbill.clients.base import BaseClient
from killbill.header import Header
from killbill.enums import Audit


class BundleClient(BaseClient):

    def list(
        self,
        header: Header,
        offset: int = 0,
        limit: int = 100,
        audit: Audit = Audit.NONE,
    ):
        """List bundles"""

        response = self._get(
            "bundles/pagination",
            headers=header.dict(),
            params={"offset": offset, "limit": limit, "audit": str(audit)},
        )

        self._raise_for_status(response)

        return response.json()

    def pause(self, header: Header, bundle_id: str, requested_date: str = None):
        """Pause a bundle"""

        response = self._put(
            f"bundles/{bundle_id}/pause",
            headers=header.dict(),
            params={"requestedDate": requested_date},
        )

        self._raise_for_status(response)

    def resume(self, header: Header, bundle_id: str, requested_date: str = None):
        """Resume a bundle"""

        response = self._put(
            f"bundles/{bundle_id}/resume",
            headers=header.dict(),
            params={"requestedDate": requested_date},
        )

        self._raise_for_status(response)
