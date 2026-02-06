import os
from dotenv import load_dotenv

load_dotenv()

def get_openai_api_key() -> str | None:
    """
    Returns OpenAI API key if available, otherwise None.
    """
    return os.getenv("OPENAI_API_KEY")
