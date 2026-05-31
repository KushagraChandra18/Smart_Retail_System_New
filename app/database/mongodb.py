from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")


print("MONGO URI =", MONGO_URI)
print("DATABASE NAME =", DATABASE_NAME)

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

sales_collection = db["sales"]

forecast_collection = db["forecasts"]

print("MongoDB Atlas Connected Successfully!")