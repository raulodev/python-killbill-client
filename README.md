# python-killbill-client

Python client for the [Kill Bill](https://killbill.io/) REST API.

> **Fork notice** — this is a fork of [raulodev/python-killbill-client](https://github.com/raulodev/python-killbill-client).

### Installation

```bash
pip install python-killbill-client
```

### Quick start

```python
from killbill import KillBillClient, Header

killbill = KillBillClient(
    username="admin",
    password="password",
    api_url="http://localhost:8080",  # default
    timeout=30,                       # default, seconds
)

header = Header(api_key="bob", api_secret="lazar", created_by="demo")
```

`KillBillClient` holds the credentials and the base URL. `Header` holds the
per-tenant credentials and audit metadata, and is passed explicitly into
almost every call — one client can therefore serve many tenants.

`Header` fields: `api_key`, `api_secret`, `created_by`, and the optional
`reason` and `comment` (sent as `X-Killbill-Reason` / `X-Killbill-Comment`).

### Recommended setup (factory with settings)

Keep credentials out of the call sites:

```python
from killbill import Header, KillBillClient

from src.settings import (
    KILLBILL_API_KEY,
    KILLBILL_API_SECRET,
    KILLBILL_API_URL,
    KILLBILL_PASSWORD,
    KILLBILL_USER,
)


def killbill():
    """Returns a KillBillClient instance and its Header"""

    client = KillBillClient(
        username=KILLBILL_USER,
        password=KILLBILL_PASSWORD,
        api_url=KILLBILL_API_URL,
    )

    header = Header(KILLBILL_API_KEY, KILLBILL_API_SECRET, "flask")

    return client, header
```

Usage:

```python
client, header = killbill()

accounts = client.account.list(header=header)
```

### Low-level client (escape hatch)

For endpoints this library does not wrap yet, subclass `BaseClient` and use
its HTTP helpers directly:

```python
from killbill.clients.base import BaseClient

from src.settings import KILLBILL_API_URL, KILLBILL_PASSWORD, KILLBILL_USER


def killbill_core():
    """Returns a raw BaseClient instance"""

    class CustomKillBillClient(BaseClient):
        def __init__(self, username, password, api_url, timeout=30):
            super().__init__(username, password, api_url, timeout)

    return CustomKillBillClient(
        username=KILLBILL_USER,
        password=KILLBILL_PASSWORD,
        api_url=KILLBILL_API_URL,
    )
```

```python
base = killbill_core()

response = base._get("accounts", headers=header.dict(), params={"limit": 10})
base._raise_for_status(response)
data = response.json()
```

`_get` / `_post` / `_put` / `_delete` take an endpoint **relative to
`/1.0/kb/`** — pass `"accounts"`, not `"/1.0/kb/accounts"`. They return the
raw `requests.Response` and do **not** raise on error; call
`_raise_for_status(response)` yourself.

Caveat: these are underscore-prefixed private methods. They are not part of
the public API and may change between versions without a major bump.

### Errors

All wrapped calls raise on non-2xx responses:

| Status | Exception         |
| ------ | ----------------- |
| 400    | `BadRequestError` |
| 401    | `AuthError`       |
| 404    | `NotFoundError`   |
| other  | `KillBillError`   |

All inherit from `KillBillError` (`killbill.exceptions`).

---

## Table of contents

- [Tenant](#tenant) — `killbill.tenant`
- [Catalog](#catalog) — `killbill.catalog`
- [Account](#account) — `killbill.account`
- [Subscription](#subscription) — `killbill.subscription`
- [Bundle](#bundle) — `killbill.bundle`
- [Invoice](#invoice) — `killbill.invoice`
- [Credit](#credit) — `killbill.credit`
- [Overdue](#overdue) — `killbill.overdue`
- [Test / clock](#test--clock) — `killbill.test`
- [Custom fields and tags](#custom-fields-and-tags)
- [Enums](#enums)

---

## Tenant

`tenant.create` is the only method that does **not** take a `Header` — it is
what produces the credentials a `Header` is built from. Returns the tenant id.

```python
killbill.tenant.create(
    api_key="bob",
    api_secret="lazar",
    created_by="demo",
    use_global_default=False,  # seed the tenant with the global default catalog
)
```

Then build the header:

```python
from killbill import Header

header = Header(api_key="bob", api_secret="lazar", created_by="demo")
```

Per-tenant system properties:

```python
killbill.tenant.retrieve_configuration(header=header)
killbill.tenant.add_configuration(header=header, config="org.killbill.foo=bar")
killbill.tenant.delete_configuration(header=header)
```

Push notification subscriptions (Kill Bill posts events to your callback):

```python
killbill.tenant.create_push_notification(header=header, callback_url="https://example.com/kb")
killbill.tenant.retrieve_push_notifications(header=header)
killbill.tenant.delete_push_notification(header=header)  # deletes all of them
```

## Catalog

#### Create a simple plan

```python
from killbill.enums import BillingPeriod, ProductCategory, TrialTimeUnit

killbill.catalog.add_simple_plan(
    header=header,
    plan_id="standard-monthly",
    product_name="Standard",
    product_category=ProductCategory.BASE,
    currency="USD",
    amount=24.95,
    billing_period=BillingPeriod.MONTHLY,
    trial_length=0,
    trial_time_unit=TrialTimeUnit.UNLIMITED,
)
```

#### Upload a catalog from a file

```python
xml_file = open("SpyCarBasic.xml", "r", encoding="utf-8").read()

killbill.catalog.validate(header=header, catalog_xml=xml_file)  # dry run
killbill.catalog.create(header=header, catalog_xml=xml_file)
```

#### Retrieve, list versions, delete

```python
catalog = killbill.catalog.retrieve(header=header)             # JSON
catalog_xml = killbill.catalog.retrieve(header=header, xml=True)

versions = killbill.catalog.versions(header=header)

killbill.catalog.delete(header=header)  # deletes ALL versions for the tenant
```

`catalog.delete` is destructive and tenant-wide. There is no per-version
delete in the Kill Bill API.

## Account

#### Create

Returns the account id.

```python
account_id = killbill.account.create(
    header=header,
    name="Customer 1",
    first_name_length=10,
    external_key="customer-1",
    email="customer1@example.com",
    currency="USD",
    bill_cycle_day_local=1,
)
```

Other accepted fields: `time_zone`, `locale`, `address1`, `address2`,
`postal_code`, `company`, `city`, `state`, `country`, `phone`, `notes`,
`is_migrated`.

#### Retrieve

```python
account = killbill.account.retrieve_by_id(header=header, account_id=account_id)
account = killbill.account.retrieve(header=header, external_key="customer-1")
```

Both accept `account_with_balance` and `account_with_balance_and_cba` — off by
default because they are expensive on Kill Bill's side.

#### List

```python
import json

accounts = killbill.account.list(header=header, offset=0, limit=100)

print(json.dumps(accounts, indent=4))
```

#### Payment methods

```python
killbill.account.add_payment_method(
    header=header,
    account_id=account_id,
    plugin_name="__EXTERNAL_PAYMENT__",
    is_default=True,
    pay_all_unpaid_invoices=False,
)

methods = killbill.account.get_payment_methods(header=header, account_id=account_id)
```

#### Payments

`payments` triggers one payment and returns the payment id.

```python
from killbill.enums import TransactionType

payment_id = killbill.account.payments(
    header=header,
    account_id=account_id,
    transaction_type=TransactionType.PURCHASE,
    amount=24.95,
)
```

`invoice_payments` pays every unpaid invoice on the account.

```python
killbill.account.invoice_payments(
    header=header,
    account_id=account_id,
    external_payment=True,
)
```

#### Invoices

```python
invoices = killbill.account.invoices(
    header=header,
    account_id=account_id,
    unpaid_invoices_only=False,
)
```

Also accepts `start_date`, `end_date`, `with_migration_invoices`,
`include_voided_invoices`, `include_invoice_components`.

#### Bundles, blocking states, overdue

```python
bundles = killbill.account.bundles(header=header, account_id=account_id)
bundles = killbill.account.bundles_pagination(header=header, account_id=account_id, limit=50)

states = killbill.account.get_blocking_states(header=header, account_id=account_id)

overdue = killbill.account.overdue(header=header, account_id=account_id)
```

#### Close

```python
killbill.account.close(
    header=header,
    account_id=account_id,
    cancel_all_subscriptions=False,
    write_off_unpaid_invoices=False,
    item_adjust_unpaid_invoices=False,
    remove_future_notifications=True,
)
```

## Subscription

#### Create

Returns the subscription id.

```python
subscription_id = killbill.subscription.create(
    header=header,
    account_id=account_id,
    plan_name="standard-monthly",
)
```

Instead of `plan_name` you may specify the plan by parts — `product_name`,
`product_category`, `billing_period`, `price_list`. Also accepts `start_date`,
`external_key` and `bundle_id`.

#### With add-ons

`create_with_add_ons` returns the bundle id.

```python
bundle_id = killbill.subscription.create_with_add_ons(
    header=header,
    account_id=account_id,
    plan_name="standard-monthly",
    add_ons_name=["standard-monthly-add-on"],
)
```

```python
killbill.subscription.create_multiple_with_add_ons(
    header,
    account_id=account_id,
    bundles=[
        ["standard-monthly", "standard-monthly-add-on"],
        ["sport-monthly", "sport-monthly-add-on-1", "sport-monthly-add-on-2"],
    ],
)
```

In each inner list the first element is the base plan; the rest are add-ons.

#### Retrieve, cancel, uncancel

```python
subscription = killbill.subscription.retrieve(header=header, subscription_id=subscription_id)
```

```python
from killbill.enums import BillingPolicy, EntitlementPolicy

killbill.subscription.cancel(
    header=header,
    subscription_id=subscription_id,
    entitlement_policy=EntitlementPolicy.END_OF_TERM,
    billing_policy=BillingPolicy.END_OF_TERM,
)

killbill.subscription.uncancel(header=header, subscription_id=subscription_id)
```

`uncancel` only works while the cancellation is still pending — once the
effective date has passed the subscription is gone for good.

#### Change the bill cycle date

```python
killbill.subscription.update_bill_cycle_date(
    header=header,
    subscription_id=subscription_id,
    day=15,
    effective_from_date=None,
    force_new_bcd_with_past_effective_date=False,
)
```

#### Blocking state

```python
killbill.subscription.block(
    header=header,
    subscription_id=subscription_id,
    state_name="SUSPENDED",
    service="my-service",
    is_block_billing=True,
)
```

## Bundle

```python
bundles = killbill.bundle.list(header=header, offset=0, limit=100)
bundle = killbill.bundle.retrieve(header=header, bundle_id=bundle_id)

killbill.bundle.pause(header=header, bundle_id=bundle_id, requested_date=None)
killbill.bundle.resume(header=header, bundle_id=bundle_id, requested_date=None)

killbill.bundle.block(
    header=header,
    bundle_id=bundle_id,
    state_name="SUSPENDED",
    service="my-service",
    is_block_billing=True,
)
```

## Invoice

```python
invoice = killbill.invoice.retrieve(
    header=header,
    invoice_id="6b8ab6a2-...",
    with_children_items=False,
)
```

To list an account's invoices use [`account.invoices`](#invoices).

## Credit

```python
killbill.credit.add(
    header=header,
    account_id=account_id,
    amount=10.00,
    currency="USD",
    description="Goodwill credit",
    auto_commit=True,
)
```

Returns the created credit items. With `auto_commit=False` the credit lands
on a DRAFT invoice and will not affect the account balance until that invoice
is committed.

## Overdue

```python
overdue_config = killbill.overdue.retrieve(header=header)          # XML string
overdue_config = killbill.overdue.retrieve(header=header, xml=False)  # JSON
```

```python
overdue_config_xml = open("Overdue.xml", "r", encoding="utf-8").read()

killbill.overdue.upload(header=header, overdue_config_xml=overdue_config_xml)
```

## Test / clock

Only available when Kill Bill runs with the test mode endpoints enabled
(`org.killbill.server.test.mode=true`). Do not point this at production.

```python
killbill.test.retrieve_clock(header=header)
killbill.test.clock(header=header, requested_date="2026-01-01")
```

## Custom fields and tags

Custom fields are supported on `account`, `subscription` and `bundle`, with
the same three methods on each.

```python
killbill.account.add_custom_fields(
    header=header,
    account_id=account_id,
    fields={"crm_id": "123", "segment": "smb"},
)

fields = killbill.account.get_custom_fields(header=header, account_id=account_id)

killbill.account.update_custom_fields(
    header=header,
    account_id=account_id,
    fields=[{"field_id": "f1e2...", "name": "segment", "value": "enterprise"}],
)
```

`add_custom_fields` takes a `dict`; `update_custom_fields` takes a list of
dicts, each requiring `field_id`, `name` and `value` — get `field_id` from
`get_custom_fields` first.

Tags are supported on `account` only:

```python
from killbill.enums import SystemTags

killbill.account.add_tags(header=header, account_id=account_id, tags=[SystemTags.AUTO_PAY_OFF])
tags = killbill.account.get_tags(header=header, account_id=account_id)
killbill.account.delete_tags(header=header, account_id=account_id, tags=[SystemTags.AUTO_PAY_OFF])
```

`SystemTags` values are Kill Bill's built-in tag definition UUIDs
(`AUTO_PAY_OFF`, `AUTO_INVOICING_OFF`, `OVERDUE_ENFORCEMENT_OFF`,
`WRITTEN_OFF`, `MANUAL_PAY`, `TEST`, `PARTNER`, `AUTO_INVOICING_DRAFT`,
`AUTO_INVOICING_REUSE_DRAFT`). For custom tags pass the tag definition id.

## Enums

All in `killbill.enums`, all `str()`-able to their wire value.

| Enum                | Values                                                                                                                                |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `Audit`             | `NONE`, `MINIMAL`, `FULL`                                                                                                             |
| `BillingPeriod`     | `DAILY`, `WEEKLY`, `BIWEEKLY`, `THIRTY_DAYS`, `THIRTY_ONE_DAYS`, `MONTHLY`, `QUARTERLY`, `BIANNUAL`, `ANNUAL`, `SESQUIENNIAL`, `BIENNIAL`, `TRIENNIAL` |
| `TrialTimeUnit`     | `UNLIMITED`, `DAYS`, `WEEKS`, `MONTHS`, `YEARS`                                                                                       |
| `ProductCategory`   | `BASE`, `ADD_ON`, `STANDALONE`                                                                                                        |
| `EntitlementPolicy` | `IMMEDIATE`, `END_OF_TERM`                                                                                                            |
| `BillingPolicy`     | `START_OF_TERM`, `END_OF_TERM`, `IMMEDIATE`, `ILLEGAL`                                                                                |
| `BlockingStateType` | `SUBSCRIPTION`, `SUBSCRIPTION_BUNDLE`, `ACCOUNT`                                                                                      |
| `TransactionType`   | `AUTHORIZE`, `CAPTURE`, `CHARGEBACK`, `PURCHASE`, `CREDIT`, `REFUND`, `VOID`                                                          |
| `State`             | `ACTIVE`, `PENDING`, `BLOCKED`, `CANCELLED`, `EXPIRED`                                                                                |
| `ObjectType`        | Kill Bill object types, used internally by the custom-field helpers                                                                   |
| `SystemTags`        | Built-in tag definition UUIDs                                                                                                         |

Dates are passed as strings in the format Kill Bill expects — `YYYY-MM-DD` for
dates, ISO 8601 for datetimes. The client does not convert `datetime` objects
for you.
