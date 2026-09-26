from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

if api_key:
    print(f"Key loaded successfully. Starts with: {api_key[:4]}...")
else:
    print("Key not found — check your .env file.")