import os

import httpx
from alterya.api import CovalentHQApi
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi import HTTPException

API_KEY = "COVALENTHQ_API_KEY"

app = FastAPI()

# noinspection PyTypeChecker
covalent_hq_client: CovalentHQApi = None  # type: ignore


async def get_client() -> CovalentHQApi:
    return covalent_hq_client


@app.on_event("startup")
async def startup_event():
    global covalent_hq_client
    load_dotenv()
    assert (key := os.environ.get(f"{API_KEY}", None)), f"ENV variable '{API_KEY}' is missing"
    await (covalent_hq_client := CovalentHQApi(api_key=key)).connect()


@app.on_event("shutdown")
async def shutdown_event():
    await covalent_hq_client.disconnect()


@app.get("/version")
async def read_version():
    return {"version": "0.0.0"}


@app.get("/v1/wallet/{wallet}/chain/{chain}/tokens")
async def read_wallet_chain_tokens(
    wallet: str, chain: str, covalent: CovalentHQApi = Depends(get_client)
):
    try:
        return await covalent.list_wallet_chain_tokens(wallet=wallet, chain=chain)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail="Remote service error: Unable to fetch data",
        )
    except Exception as _:
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to parse data")


@app.get("/v1/wallet/{wallet}/chain/{chain}/transactions/{page}")
async def read_wallet_chain_transactions_paged(
    wallet: str, chain: str, page: int, covalent: CovalentHQApi = Depends(get_client)
):
    try:
        return await covalent.list_wallet_chain_tokens(wallet=wallet, chain=chain, page=page)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail="Remote service error: Unable to fetch data",
        )
    except Exception as _:
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to parse data")


@app.get("/v1/wallet/{wallet}/chain/{chain}/balance/{currency}")
async def read_wallet_chain_usd_balance(
    wallet: str,
    chain: str,
    currency: str,
    covalent: CovalentHQApi = Depends(get_client),
):
    try:
        assert str(currency).lower() == "usd", "Currently ony USD is supported"
        return await covalent.get_wallet_chain_usd_balance(wallet=wallet, chain=chain, currency=currency)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail="Remote service error: Unable to fetch data",
        )
    except Exception as _:
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to parse data")
