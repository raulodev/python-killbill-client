import enum


class Audit(enum.Enum):
    """Account Audit"""

    NONE = "NONE"
    MINIMAL = "MINIMAL"
    FULL = "FULL"

    def __str__(self):
        return self.value


class BillingPeriod(enum.Enum):
    """Billing Period"""

    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    BIWEEKLY = "BIWEEKLY"
    THIRTY_DAYS = "THIRTY_DAYS"
    THIRTY_ONE_DAYS = "THIRTY_ONE_DAYS"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    BIANNUAL = "BIANNUAL"
    ANNUAL = "ANNUAL"
    SESQUIENNIAL = "SESQUIENNIAL"
    BIENNIAL = "BIENNIAL"
    TRIENNIAL = "TRIENNIAL"

    def __str__(self):
        return self.value


class TrialTimeUnit(enum.Enum):
    """Trial Time Unit"""

    UNLIMITED = "UNLIMITED"
    DAYS = "DAYS"
    WEEKS = "WEEKS"
    MONTHS = "MONTHS"
    YEARS = "YEARS"

    def __str__(self):
        return self.value


class ProductCategory(enum.Enum):
    """Product Category"""

    BASE = "BASE"
    ADD_ON = "ADD_ON"
    STANDALONE = "STANDALONE"

    def __str__(self):
        return self.value


class EntitlementPolicy(enum.Enum):
    """Entitlement Policy"""

    IMMEDIATE = "IMMEDIATE"
    END_OF_TERM = "END_OF_TERM"

    def __str__(self):
        return self.value


class BillingPolicy(enum.Enum):
    """Billing Policy"""

    START_OF_TERM = "START_OF_TERM"
    END_OF_TERM = "END_OF_TERM"
    IMMEDIATE = "IMMEDIATE"
    ILLEGAL = "ILLEGAL"

    def __str__(self):
        return self.value


class BlockingStateType(enum.Enum):
    """Blocking State Type"""

    SUBSCRIPTION = "SUBSCRIPTION"
    SUBSCRIPTION_BUNDLE = "SUBSCRIPTION_BUNDLE"
    ACCOUNT = "ACCOUNT"

    def __str__(self):
        return self.value


class ObjectType(enum.Enum):
    """Object Type"""

    ACCOUNT = "ACCOUNT"
    ACCOUNT_EMAIL = "ACCOUNT_EMAIL"
    BLOCKING_STATES = "BLOCKING_STATES"
    BUNDLE = "BUNDLE"
    CUSTOM_FIELD = "CUSTOM_FIELD"
    INVOICE = "INVOICE"
    PAYMENT = "PAYMENT"
    TRANSACTION = "TRANSACTION"
    INVOICE_ITEM = "INVOICE_ITEM"
    INVOICE_PAYMENT = "INVOICE_PAYMENT"
    SUBSCRIPTION = "SUBSCRIPTION"
    SUBSCRIPTION_EVENT = "SUBSCRIPTION_EVENT"
    SERVICE_BROADCAST = "SERVICE_BROADCAST"
    PAYMENT_ATTEMPT = "PAYMENT_ATTEMPT"
    PAYMENT_METHOD = "PAYMENT_METHOD"
    TAG = "TAG"
    TAG_DEFINITION = "TAG_DEFINITION"
    TENANT = "TENANT"
    TENANT_KVS = "TENANT_KVS"

    def __str__(self):
        return self.value


class TransactionType(enum.Enum):
    """Transaction Type"""

    AUTHORIZE = "AUTHORIZE"
    CAPTURE = "CAPTURE"
    CHARGEBACK = "CHARGEBACK"
    PURCHASE = "PURCHASE"
    CREDIT = "CREDIT"
    REFUND = "REFUND"
    VOID = "VOID"

    def __str__(self):
        return self.value


class State(enum.Enum):
    """State"""

    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

    def __str__(self):
        return self.value


class SystemTags(enum.Enum):

    AUTO_PAY_OFF = "00000000-0000-0000-0000-000000000001"
    """Suspends payments until removed."""

    AUTO_INVOICING_OFF = "00000000-0000-0000-0000-000000000002"
    """Suspends invoicing until removed."""

    OVERDUE_ENFORCEMENT_OFF = "00000000-0000-0000-0000-000000000003"
    """Suspends overdue enforcement behaviour until removed."""

    WRITTEN_OFF = "00000000-0000-0000-0000-000000000004"
    """Indicates that an invoice is written off. This has no effect on billing or payment."""

    MANUAL_PAY = "00000000-0000-0000-0000-000000000005"
    """Indicates that Killbill doesn't process payments for this account. 
    That is, the account uses external payments only.
    """

    TEST = "00000000-0000-0000-0000-000000000006"
    """Indicates that this is a test account."""

    PARTNER = "00000000-0000-0000-0000-000000000007"
    """Indicates that this is a partner account."""

    AUTO_INVOICING_DRAFT = "00000000-0000-0000-0000-000000000008"
    """Generate account invoices in DRAFT mode."""

    AUTO_INVOICING_REUSE_DRAFT = "00000000-0000-0000-0000-000000000009"
    """Use existing draft invoice if exists."""

    def __str__(self):
        return self.value
