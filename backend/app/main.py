from fastapi import FastAPI

app = FastAPI(title="MatDeal API")

@app.get("/health")
async def health():
    return {"status": "ok"}