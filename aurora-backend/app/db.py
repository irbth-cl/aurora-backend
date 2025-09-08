# app/db.py
from supabase import create_client
import os

# Get Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Store a new fact/article in Supabase
def store_fact(url, summary, trust_score=0.5):
    supabase.table("facts").insert({
        "source_url": url,
        "summary": summary,
        "trust_score": trust_score
    }).execute()

# Retrieve the most recent facts/articles
def get_recent_facts(limit=10):
    response = supabase.table("facts")\
        .select("*")\
        .order("first_seen", desc=True)\
        .limit(limit)\
        .execute()
    return response.data
