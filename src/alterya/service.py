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


@app.get("/v1/asset/token/list/wallet/{wallet}/chain/{chain}")
async def read_chain_token_list(
    wallet: str, chain: str, covalent: CovalentHQApi = Depends(get_client)
):
    try:
        return await covalent.list_chain_tokens(wallet=wallet, chain=chain)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail="Remote service error: Unable to fetch data",
        )
    except Exception as _:
        raise HTTPException(status_code=500, detail="Internal Server Error: Unable to parse data")
