import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
MONGO_URL = os.getenv("MONGO_URL")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


# Define the configuration for the scraping pipeline
graph_config = {
    "llm": {
        "api_key": OPENAI_KEY,
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": True,
}

links_to_scrape = {
    "toycollectorsindia": "https://www.toycollectorsindia.com/collections/mini-gt?filter.v.price.gte=&filter.v.price.lte=&sort_by=created-descending",
    "tooneywheels": "https://tooneywheels.in/brand/mini-gt/?orderby=date",
    "karzanddolls": "https://www.karzanddolls.com/details/mini+gt+/mini-gt/MTY1",
}
