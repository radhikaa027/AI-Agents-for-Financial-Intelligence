import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

LLM_MODEL = os.getenv("LLM_MODEL", "gemini/gemini-2.5-flash")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))

DEFAULT_COMPANY = os.getenv("DEFAULT_COMPANY", "TSLA")
ANALYSIS_PERIOD = os.getenv("ANALYSIS_PERIOD", "1y")
NEWS_LOOKBACK_DAYS = int(os.getenv("NEWS_LOOKBACK_DAYS", "7"))

MCP_ENABLED = True
A2A_PROTOCOL_ENABLED = True

OUTPUT_FORMAT = "markdown"
REPORT_TEMPLATE = "investment_report"

def validate_config():
    """Validate that all required configurations are set"""
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY not found in environment variables")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    print("✅ Configuration validated successfully!")
    return True