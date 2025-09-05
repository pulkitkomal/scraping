import datetime, re
from pymongo import MongoClient
from src.utils.configs import MONGO_URL, logger


class Mongo:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        db = self.client['Cluster0']
        self.diecast_data = db['diecast_data']
        self.tokens_metadata = db['tokens_metadata']

    def insert_token_data(self, data):
        try:
            self.tokens_metadata.insert_one(data)
            return True
        except Exception as e:
            logger.exception(f'Error occured: {e}')
            return False
    
    def insert_many_diecast(self, data):
        try:
            self.diecast_data.insert_many(data)
            logger.info(f'Total data inserted {data.__len__()}')
            return True
        except Exception as e:
            logger.exception(f'Error occured: {e}')
            return False
        
    def find_many_diecast(self, query):
        try:
            cars_exist = []
            data = self.diecast_data.find(query)
            if data:
                for d in data:
                    cars_exist.append(d['car_name'])
            return cars_exist
        except Exception as e:
            logger.exception(f'Error occured: {e}')
            return {}
        
    def read_data_diecast(self, hours):
        car_names = []
        last_day = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=hours)
        cursor = self.diecast_data.find({"created_at": {"$gte": last_day}})
        for document in cursor:
            car_names.append((document['car_name'], document['website']))
        return car_names
    
    def read_individual_car_diecast(self, name, minutes):
        car_names = []
        time_delta = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=minutes)

        pattern = re.compile(name, re.IGNORECASE)
        cursor = self.diecast_data.find({'car_name': {'$regex': pattern}, "created_at": {"$gte": time_delta}})
        for document in cursor:
            car_names.append((document['car_name'], document['website']))
        return car_names


mongo = Mongo()