from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "financial_assistant"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

parents_collection = db["parents"]
reminders_collection = db["reminders"]
