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
