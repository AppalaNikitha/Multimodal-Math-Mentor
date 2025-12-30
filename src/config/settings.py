from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    groq_api_key = os.getenv("GROQ_API_KEY")
    groq_model = "llama3-70b-8192"

settings = Settings()

AGENT_CONFIG = {
    "solver": {
        "temperature": 0.2,
        "max_tokens": 1024
    }
}
