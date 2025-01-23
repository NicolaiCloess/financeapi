import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
METALS_API_KEY = os.getenv("METALS_API_KEY")
FIXER_API_KEY = os.getenv("FIXER_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
COINGECKO_API_KEY= os.getenv("COINGECKO_API_KEY")
