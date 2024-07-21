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

    async def assert_inputs(self, chain, wallet):
        assert (chain := chain or self.chain), "Chain is not set for the API call"
        assert (wallet := wallet or self.wallet), "Wallet is set for the API call"
        assert (chain := str(chain).strip()), "Chain is not set for the API call"
        assert (wallet := str(wallet).strip()), "Wallet is not set for the API call"
        return chain, wallet

    async def list_wallet_chain_tokens(
        self,
        chain: str | None = None,
        wallet: str | None = None,
    ) -> list[dict]:
        chain, wallet = await self.assert_inputs(chain, wallet)
        endpoint = self.base_url.child(chain, "address", wallet, "balances_v2", "").to_text()
        response = await self.client.get(endpoint)
        return response.raise_for_status().json().get("data", {}).get("items", [])

    async def list_wallet_chain_transactions_paged(
        self,
        chain: str | None = None,
        wallet: str | None = None,
        page: int = 0,
    ) -> list[dict]:
        chain, wallet = await self.assert_inputs(chain, wallet)
        assert (page := str(page)).isnumeric(), "Page is not a number"
        endpoint = self.base_url.child(
            chain, "address", wallet, "transactions_v3", "page", page, ""
        ).to_text()
        # I didn't get real data sample so I am guessing it will have similar structure $.data.items
        response = await self.client.get(endpoint)
        return response.raise_for_status().json().get("data", {}).get("items", [])

    async def get_wallet_chain_usd_balance(
        self, chain: str | None = None, wallet: str | None = None, currency: str = "USD"
    ) -> float:
        items = await self.list_wallet_chain_tokens(chain, wallet)
        return sum(it.get("quote", 0.0) or 0.0 for it in items)
