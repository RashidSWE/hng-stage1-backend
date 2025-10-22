from pymongo import MongoClient
from dotenv import load_dotenv
import os

db_url = os.getenv("MONGO_URL")


try:
    client = MongoClient(db_url)
except EXCEPTION  as e:
    print("error", e)

db_client = client.hng_db

string_collection = db_client['text']