import httpx
from hyperlink import URL


class CovalentHQApi:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.covalenthq.com/v1/",
        chain: str | None = None,
        wallet: str | None = None,
    ):
        self.api_key = api_key
        self.base_url = URL.from_text(base_url)
        self.chain = chain
        self.wallet = wallet
        self.client = None
        self.default_headers = {"Content-Type": "application/json", "Accept": "application/json"}

    async def connect(self):
        self.client = httpx.AsyncClient(
            base_url=self.base_url.to_text(),
            auth=(self.api_key, ""),
            headers=self.default_headers,
        )
        return self

    async def disconnect(self):
        await self.client.aclose()

    async def list_chain_tokens(
        self,
        chain: str | None = None,
        wallet: str | None = None,
    ) -> dict:
        assert (chain := chain or self.chain), "Chain is not set for the API call"
        assert (wallet := wallet or self.wallet), "Wallet is set for the API call"

        endpoint = self.base_url.child(chain, "address", wallet, "balances_v2", "").to_text()
        return (await self.client.get(endpoint)).raise_for_status().json()
