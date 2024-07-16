# mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

mongodb_url =  os.getenv('MONGODB_URL')
database= os.getenv('DATABASE')
client = AsyncIOMotorClient(mongodb_url)
database = client[database]
collection_amortizacion = os.getenv('COLLECTION_AMORTIZACION')
amortizacion_collection = database[collection_amortizacion]
