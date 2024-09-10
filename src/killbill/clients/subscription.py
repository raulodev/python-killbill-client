from killbill.clients.base import BaseClient
from killbill.header import Header
from killbill.enums import Audit, EntitlementPolicy, BillingPolicy


class Subscription(BaseClient):

    def create(
        self,
        header: Header,
        account_id: str,
        plan_name: str,
        start_date: str = None,
    ):
        """Create an subscription

        Returns:
            str or None: The subscription's ID or None if the request failed.
        """

        payload = {
            "accountId": account_id,
            "planName": plan_name,
            "startDate": start_date,
        }

        response = self._post("subscriptions", headers=header.dict(), payload=payload)

        self._raise_for_status(response)

        return self._get_uuid(response.headers.get("Location"))

    def retrieve(self, header: Header, subscription_id: str, audit: Audit = Audit.NONE):
        """Retrieve a subscription by id"""

        response = self._get(
            f"subscriptions/{subscription_id}",
            headers=header.dict(),
            params={"audit": str(audit)},
        )

        self._raise_for_status(response)

        return response.json()

    def cancel(
        self,
        header: Header,
        subscription_id: str,
        requested_date: str = None,
        use_requested_date_for_billing: bool = False,
        entitlement_policy: EntitlementPolicy = None,
        billing_policy: BillingPolicy = None,
    ):
        """Cancel an entitlement plan"""

        response = self._delete(
            f"subscriptions/{subscription_id}",
            headers=header.dict(),
            params={
                "requestedDate": requested_date,
                "entitlementPolicy": str(entitlement_policy),
                "billingPolicy": str(billing_policy),
                "useRequestedDateForBilling": use_requested_date_for_billing,
            },
        )

        self._raise_for_status(response)

    def uncancel(self, header: Header, subscription_id: str):
        """Un-cancel an entitlement"""

        response = self._put(
            f"subscriptions/{subscription_id}/uncancel",
            headers=header.dict(),
        )

        self._raise_for_status(response)
