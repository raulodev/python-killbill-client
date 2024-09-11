# python-killbill-client

### Guide

Frist step create client

```python
from killbill import KillBillClient

killbill = KillBillClient("admin", "password")
```

Table of contents :

- [Tenant](#tenant)
- [Catalog](#catalog)
- [Account](#account)
- [Subscription](#subscription)
- [Invoices](#invoices)
- [Overdue](#overdue)

## Tenant

Create a tenant

```python
killbill.tenant.create(api_key="bob", api_secret="lazar", created_by="demo")
```

And use `api_key` and `api_secret` to create header

```python
from killbill import Header

header = Header(api_key="bob", api_secret="lazar", created_by="demo")
```

## Catalog

Create a simple catalog

```python
from killbill.enums import ProductCategory, BillingPeriod, TrialTimeUnit

killbill.catalog.add_simple_plan(
    header=header, # pass header
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

Create a catalog from file

```python
# first get text content
xml_file = open("SpyCarBasic.xml", "r", encoding="utf-8").read()

killbill.catalog.create(header=header, catalog_xml=xml_file)
```

## <a name="account"></a> Account

Create account

```python
# return account id
account_id = killbill.account.create(
    header=header,
    name="Customer 1",
    first_name_length=10,
)
```

List accounts

```python
import json

accounts = killbill.account.list(header=header)

print(json.dumps(accounts, indent=4))
```

Add a payment method to the account

Note: Replace `3d52ce98-104e-4cfe-af7d-732f9a264a9a` below with the ID of your account.

```python
killbill.account.add_payment_method(
    header=header,
    account_id="3d52ce98-104e-4cfe-af7d-732f9a264a9a",
    plugin_name="__EXTERNAL_PAYMENT__",
    is_default=True,
)
```

## <a name="subscription"></a> Subscription

Set Up a Subscription for the Account

Note: Replace `3d52ce98-104e-4cfe-af7d-732f9a264a9a` below with the ID of your account.

```python
subscription_id = killbill.subscription.create(
    header=header,
    account_id="3d52ce98-104e-4cfe-af7d-732f9a264a9a",
    plan_name="standard-monthly",
)
```

## <a name="invoices"></a> Invoices

Retrieve account invoices

Note: Replace `3d52ce98-104e-4cfe-af7d-732f9a264a9a` below with the ID of your account.

```python
invoices = killbill.account.invoices(
    header=header, account_id="3d52ce98-104e-4cfe-af7d-732f9a264a9a"
)

print(json.dumps(invoices, indent=4))
```

## <a name="overdue"></a> Overdue

Retrieve overdue config

```python
overdue_config = killbill.overdue.retrieve(header=header)

print(overdue_config)
```

Upload overdue config

```python
# first get text content
overdue_config_xml = open("Overdue.xml", "r", encoding="utf-8").read()

killbill.overdue.upload(header=header, overdue_config_xml=overdue_config_xml)
```
