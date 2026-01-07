from fastapi import FastAPI, Request, HTTPException
import json
import os
from datetime import datetime
from ai_responder import generate_ticket_reply

app = FastAPI()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET") # check the node in the fresh service workflow (remember that this is the security we are using now)
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
    ai_reply = generate_ticket_reply(data)
    
    with open("webhook_log.json", "a") as f:
        f.write(json.dumps({
            "received_at": str(datetime.now()),
            "request": data,
            "ai_reply": ai_reply,
        }) + "\n")

    return {
        "status": "success",
        "message": "Webhook received!",
        "ai_reply":ai_reply,
        "received_data": data
    }
@app.get("/health")
async def health_check():
    return {"status": "ok"}
