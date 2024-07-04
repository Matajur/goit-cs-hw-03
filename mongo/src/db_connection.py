"""Module that provides connection with MongoDB"""

import configparser
from pymongo import MongoClient

config = configparser.ConfigParser()
config.read("config.ini")

username = config.get("DB", "user")
password = config.get("DB", "pass")
domain = config.get("DB", "domain")
port = config.get("DB", "port")
db_name = config.get("DB", "db_name")
collect = config.get("DB", "collect")

client = MongoClient(f"mongodb://{username}:{password}@{domain}:{port}/")
db = client[db_name]
collection = db[collect]
