from datetime import datetime
import pytz

from src.utils.configs import links_to_scrape, logger
from src.utils.db import mongo
from src.modules.smart_scrapper import SmartScraper


class DiecastScraper:
    def __init__(self):
        self.all_data = {}
        self.total_token_used = 0
        self.total_cost = 0

    def scrape_diecast_info(self, bot, chat_id):
        for website, link in links_to_scrape.items():
            bot.send_chat_action(chat_id, "typing")
            logger.info(f"{website} ---- {link}")
            bot.send_message(chat_id, f"Scrapping {website} !!")
            smart_scraper = SmartScraper(source=link)
            try:
                self.all_data[website] = smart_scraper.run().get("content")
                bot.send_chat_action(chat_id, "typing")
                bot.send_message(chat_id, f"Cars found for {website} {len(self.all_data[website])}")
            except:
                continue
            for execution_stats in smart_scraper.get_execution_info():
                if execution_stats["node_name"] == "TOTAL RESULT":
                    self.total_token_used += execution_stats["total_tokens"]
                    self.total_cost += execution_stats["total_cost_USD"]

        logger.info(
            f"total tokens: {self.total_token_used}, total_cost: {self.total_cost}"
        )
        india_tz = pytz.timezone("Asia/Kolkata")
        utc_time = datetime.now(pytz.utc)
        india_time = utc_time.astimezone(india_tz)
        mongo.insert_token_data(
            {
                "total_tokens": self.total_token_used,
                "total_cost": self.total_cost,
                "created_at": india_time,
            }
        )
        return {
            "total_token_used": self.total_token_used,
            "total_cost": self.total_cost,
        }

    def write_to_mongo(self):
        records = []
        for website, data_items in self.all_data.items():
            cars_exist = mongo.find_many_diecast(query={"website": website})
            if not isinstance(data_items, list):
                continue
            for data in data_items:
                india_tz = pytz.timezone("Asia/Kolkata")
                utc_time = datetime.now(pytz.utc)
                india_time = utc_time.astimezone(india_tz)
                if data["Name"] in cars_exist:
                    continue
                record = {
                    "car_name": data["Name"],
                    "price": data["Price"],
                    "website": website,
                    "created_at": india_time,
                }

                records.append(record)
        if records:
            mongo.insert_many_diecast(data=records)
        else:
            logger.info("No Records to insert..")

        return records
