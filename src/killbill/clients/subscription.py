from typing import List
from killbill.clients.base import BaseClient
from killbill.header import Header
from killbill.enums import (
    Audit,
    EntitlementPolicy,
    BillingPolicy,
    ProductCategory,
    BillingPeriod,
    ObjectType,
)


class SubscriptionClient(BaseClient):

    def create(
        self,
        header: Header,
        account_id: str,
        plan_name: str,
        start_date: str = None,
        external_key: str = None,
        product_name: str = None,
        product_category: ProductCategory = None,
        billing_period: BillingPeriod = None,
        price_list: str = None,
    ):
        """Create an subscription

        Returns:
            str or None: The subscription's ID or None if the request failed.
        """

        payload = {
            "accountId": account_id,
            "planName": plan_name,
            "externalKey": external_key,
            "productName": product_name,
            "productCategory": str(product_category) if product_category else None,
            "billingPeriod": str(billing_period) if billing_period else None,
            "priceList": price_list,
        }

        params = {
            "entitlementDate": start_date,
            "billingDate": start_date,
        }

        response = self._post(
            "subscriptions", headers=header.dict(), payload=payload, params=params
        )

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

        params = {
            "requestedDate": requested_date,
            "entitlementPolicy": (
                str(entitlement_policy) if entitlement_policy else None
            ),
            "billingPolicy": str(billing_policy) if billing_policy else None,
            "useRequestedDateForBilling": use_requested_date_for_billing,
        }

        response = self._delete(
            f"subscriptions/{subscription_id}",
            headers=header.dict(),
            params=params,
        )

        self._raise_for_status(response)

    def uncancel(self, header: Header, subscription_id: str):
        """Un-cancel an entitlement"""

        response = self._put(
            f"subscriptions/{subscription_id}/uncancel",
            headers=header.dict(),
        )

        self._raise_for_status(response)

    def create_with_add_ons(
        self,
        header: Header,
        account_id: str,
        plan_name: str,
        add_ons_name: list[str],
        start_date: str = None,
    ):
        """Create an entitlement with addOn products

        Args:
            add_ons_name (list[str]): List of add-ons (plan name) to be added to the subscription

        Returns:
            str or None: The bundle's ID or None if the request failed.
        """

        payload = [
            {
                "accountId": account_id,
                "planName": plan_name,
            }
        ]

        params = {"entitlementDate": start_date, "billingDate": start_date}

        for add_ons in add_ons_name:
            payload.append(
                {
                    "accountId": account_id,
                    "planName": add_ons,
                }
            )

        response = self._post(
            "subscriptions/createSubscriptionWithAddOns",
            headers=header.dict(),
            payload=payload,
            params=params,
        )

        self._raise_for_status(response)

        return self._get_uuid(response.headers.get("Location"))

    def create_multiple_with_add_ons(
        self,
        header: Header,
        account_id: str,
        bundles: list[list],
        start_date: str = None,
    ):
        """Create multiple entitlements with addOn products

        >> Example
        ```python
        killbill.subscription.create_multiple_with_add_ons(
            header,
            account_id="3d52ce98-104e-4cfe-af7d-732f9a264a9a",
            bundles=[
                ["standard-monthly", "standard-monthly-add-on"],
                ["sport-monthly", "sport-monthly-add-on-1", "sport-monthly-add-on-2"],
            ],
        )
        ```
        """

        payload = []

        for bundle in bundles:
            base_and_add_ons = []
            for plan in bundle:
                base_and_add_ons.append(
                    {
                        "accountId": account_id,
                        "planName": plan,
                    }
                )

            payload.append({"baseEntitlementAndAddOns": base_and_add_ons})

        params = {"entitlementDate": start_date, "billingDate": start_date}

        response = self._post(
            "subscriptions/createSubscriptionsWithAddOns",
            headers=header.dict(),
            payload=payload,
            params=params,
        )

        self._raise_for_status(response)

    def add_custom_fields(
        self,
        header: Header,
        subscription_id: str,
        fields: dict,
        object_type: ObjectType = ObjectType.ACCOUNT,
    ):
        """Add custom fields to subscription"""

        payload = []

        for item in fields.items():
            payload.append(
                {
                    "objectType": str(object_type),
                    "name": item[0],
                    "value": item[1],
                }
            )

        response = self._post(
            f"subscriptions/{subscription_id}/customFields",
            headers=header.dict(),
            payload=payload,
        )

        self._raise_for_status(response)

    def get_custom_fields(
        self, header: Header, subscription_id: str, audit: Audit = Audit.NONE
    ):
        """Retrieve subscription custom fields"""

        params = {"audit": str(audit)}

        response = self._get(
            f"subscriptions/{subscription_id}/customFields",
            headers=header.dict(),
            params=params,
        )

        self._raise_for_status(response)

        return response.json()

    def update_custom_fields(
        self,
        header: Header,
        subscription_id: str,
        fields: List[dict],
        object_type: ObjectType = ObjectType.ACCOUNT,
    ):
        """Modify custom fields to subscription


        ```python
        killbill.subscription.update_custom_fields(
            header,
            subscription_id="subscription_id",
            object_type=ObjectType.SUBSCRIPTION,
            fields=[
                {
                    "name": "name",
                    "value": "value",
                    "field_id": "field_id",
                }
            ],
        )

        ```
        """

        if not isinstance(fields, (list, tuple)):
            raise TypeError("fields must be a list or tuple")

        for item in fields:
            if not isinstance(item, dict):
                raise TypeError("fields must be a list of dict")

            if not item.get("name"):
                raise ValueError("name is required")

            if not item.get("value"):
                raise ValueError("value is required")

            if not item.get("field_id"):
                raise ValueError("field_id is required")

        payload = []

        for item in fields:
            payload.append(
                {
                    "objectType": str(object_type),
                    "name": item.get("name"),
                    "value": item.get("value"),
                    "customFieldId": item.get("field_id"),
                }
            )

        response = self._put(
            f"subscriptions/{subscription_id}/customFields",
            headers=header.dict(),
            payload=payload,
        )

        self._raise_for_status(response)
