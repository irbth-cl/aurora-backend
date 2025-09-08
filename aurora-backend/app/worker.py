# app/worker.py
import asyncio
from app.db import store_fact, get_recent_facts
import datetime

async def decision_loop():
    """
    Aurora's autonomous loop:
    - Fetches or generates new facts
    - Stores them in Supabase
    - Logs actions
    """
    while True:
        try:
            # Example: mock candidate facts
            candidates = [
                {"url": "https://example.com/article1", "summary": "Sample fact 1"},
                {"url": "https://example.com/article2", "summary": "Sample fact 2"}
            ]

            for c in candidates:
                store_fact(c["url"], c["summary"])
                print(f"[{datetime.datetime.now()}] Stored fact: {c['summary']}")

            # Optional: fetch recent facts for verification
            recent = get_recent_facts(limit=5)
            print(f"[{datetime.datetime.now()}] Recent facts count: {len(recent)}")

            # Sleep for 1 hour before next loop (3600 seconds)
            await asyncio.sleep(3600)

        except Exception as e:
            print(f"[{datetime.datetime.now()}] Error in loop: {e}")
            await asyncio.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    print("Aurora worker started...")
    asyncio.run(decision_loop())
