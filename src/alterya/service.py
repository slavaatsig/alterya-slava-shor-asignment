from fastapi import FastAPI

app = FastAPI()


@app.get("/version")
async def read_version():
    return {"version": "0.0.0"}
