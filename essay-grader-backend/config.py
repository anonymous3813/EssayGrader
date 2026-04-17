from dotenv import load_dotenv
import os
from google import genai
from supabase import create_client, Client
from pathlib import Path

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key=api_key)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)


BASE_DIR = Path(__file__).resolve().parent