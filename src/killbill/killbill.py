from .clients.tenant import TenantClient
from .clients.catalog import CatalogClient
from .clients.account import AccountClient
from .clients.subscription import Subscription
from .clients.bundle import BundleClient


class KillBillClient:
    """Kill Bill Client"""

    def __init__(
        self,
        username: str,
        password: str,
        api_url: str = "http://localhost:8080",
    ):
        self.tenant = TenantClient(username, password, api_url)
        self.catalog = CatalogClient(username, password, api_url)
        self.account = AccountClient(username, password, api_url)
        self.subscription = Subscription(username, password, api_url)
        self.bundle = BundleClient(username, password, api_url)
