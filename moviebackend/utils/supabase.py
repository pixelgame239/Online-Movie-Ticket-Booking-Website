from datetime import datetime
from supabase import create_client
import os

SUPABASE_URL = "https://anxkatxbafgpahipxzsw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFueGthdHhiYWZncGFoaXB4enN3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc5MjM1ODIsImV4cCI6MjA3MzQ5OTU4Mn0.y5Iai5ZRM0Wbk2YM8BypEqWMUkw-MTizVJnY0bCkPbo"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_to_supabase(file_obj, path_in_bucket, bucket_name):
    sanitized_path = path_in_bucket.replace(" ", "_")
    try:
        response = supabase.storage.from_(bucket_name).upload(
            path=sanitized_path,
            file=file_obj,
            file_options={"upsert":"true"},
        )
    except Exception as e:
        print(f"[Supabase Upload] Exception during upload call: {e}")
        raise

    if response is None:
        raise Exception("Supabase response was None")

    if isinstance(response, dict) and response.get("error"):
        err = response.get("error")
        print(f"[Supabase Upload] Response error: {err}")
        raise Exception(f"Upload failed: {err}")
    try:
        public_response = supabase.storage.from_(bucket_name).get_public_url(sanitized_path)
    except Exception as e:
        print(f"[Supabase Upload] Exception getting public URL: {e}")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    url = f"{public_response}?v={timestamp}"
    if not url:
        raise Exception(f"Could not get public URL from: {public_response}")

    return url