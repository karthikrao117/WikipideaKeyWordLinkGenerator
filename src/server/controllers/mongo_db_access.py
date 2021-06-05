import logging
from pymongo import MongoClient
import os

class DBConnection:
    """
    Establish connection update later
    """
    client = None
    collection = None
    
    def __init__(self) -> None:
        pass

    @classmethod
    def establish_connection(cls):
        try:
            cls.client = MongoClient("mongodb+srv://"+os.getenv('MONGO_USERNAME')+":"+os.getenv('MONGO_PASSWORD')+"@cluster0.i3pu3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            db = cls.client['wikilink']
            cls.collection = db['wikiLinkcollection']
        except Exception as error:
            logging.error("Error occured while connecting to DB::"+str(error))
    
    @classmethod
    def db_update_collection_data(cls,keyword,keyLinkList):
        try:
            logging.info("db_update_collection_data ::updation Key "+str(keyword))
            cls.collection.insert({'_id':keyword,'links':keyLinkList})
        except Exception as error:
            logging.error("Error occured while connecting to DB db_update_collection_data::"+str(error))

    @classmethod
    def wiki_link_exists(cls,keyword):
        try:
            logging.info("wiki_link_exists search Key"+str(keyword))
            if cls.collection.find({'_id':keyword}).count() > 0:
                return True
            return False
        except Exception as error:
            logging.error("Error occured while connecting to DB wiki_link_exists::"+str(error))
            return False