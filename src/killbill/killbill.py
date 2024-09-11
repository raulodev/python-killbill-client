from killbill.clients.tenant import TenantClient
from killbill.clients.catalog import CatalogClient
from killbill.clients.account import AccountClient
from killbill.clients.subscription import Subscription
from killbill.clients.bundle import BundleClient
from killbill.clients.overdue import OverdueClient


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
        self.overdue = OverdueClient(username, password, api_url)
