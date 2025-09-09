import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from app.db import store_fact, get_recent_facts
import threading
import datetime

app = FastAPI(title="Aurora")

class ChatMessage(BaseModel):
    message: str

# Chat API endpoints
@app.get("/")
def root():
    return {"message": "Aurora is alive!"}

@app.post("/chat")
def chat(msg: ChatMessage):
    user_message = msg.message
    store_fact("user_message", user_message)
    reply = f"Aurora received: '{user_message}'"
    print(f"[{datetime.datetime.now()}] Chat: {user_message} -> {reply}")
    return {"reply": reply}

# Autonomous loop
async def decision_loop():
    while True:
        try:
            candidates = [
                {"url": "https://example.com/article1", "summary": "Sample fact 1"},
                {"url": "https://example.com/article2", "summary": "Sample fact 2"}
            ]
            for c in candidates:
                store_fact(c["url"], c["summary"])
                print(f"[{datetime.datetime.now()}] Stored fact: {c['summary']}")
            await asyncio.sleep(3600)
        except Exception as e:
            print(f"[{datetime.datetime.now()}] Error: {e}")
            await asyncio.sleep(60)

# Run the loop in a separate thread
def start_loop():
    asyncio.run(decision_loop())

threading.Thread(target=start_loop, daemon=True).start()
