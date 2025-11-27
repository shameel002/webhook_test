from fastapi import FastAPI, Request, HTTPException
import json
from datetime import datetime

app = FastAPI()

WEBHOOK_SECRET = "123456secret"  # must match Freshservice header

def verify_secret(request: Request):
    received_secret = request.headers.get("X-Webhook-Secret")
    if received_secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized webhook request")

@app.post("/webhook/freshservice")
async def receive_webhook(request: Request):
    verify_secret(request)

    data = await request.json()
    print("\n📩 Webhook Data Received:")
    print(json.dumps(data, indent=4))

    return {
        "status": "success",
        "message": "Webhook received!",
        "received_data": data
    }
