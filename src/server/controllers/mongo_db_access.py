import logging
from pymongo import MongoClient
import os

class DBConnection:
    """
    Establish connection update later
    """
    client = None
    collection = None
    database = None
    def __init__(self) -> None:
        pass

    @classmethod
    def establish_connection(cls):
        try:
            cls.client = MongoClient("mongodb+srv://"+os.getenv('MONGO_USERNAME')+":"+os.getenv('MONGO_PASSWORD')+"@cluster0.i3pu3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            cls.database = cls.client['wikilink']
        except Exception as error:
            logging.error("Error occured while connecting to DB::"+str(error))
    
    @classmethod
    def db_update_wiki_collection_data(cls,keyword,keyLinkList):
        try:
            logging.info("db_update_collection_data ::updation Key "+str(keyword))
            cls.collection = cls.database['wikiLinkcollection']
            cls.collection.insert({'_id':keyword,'links':keyLinkList})
        except Exception as error:
            logging.error("Error occured while connecting to DB db_update_collection_data::"+str(error))

    @classmethod
    def wiki_link_exists(cls,keyword):
        try:
            logging.info("wiki_link_exists search Key"+str(keyword))
            cls.collection = cls.database['wikiLinkcollection']
            if cls.collection.find({'_id':keyword}).count() > 0:
                return True
            return False
        except Exception as error:
            logging.error("Error occured while connecting to DB wiki_link_exists::"+str(error))
            return False
    
    @classmethod
    def get_wiki_link_list(cls,keyword):
        output_data = {}
        try:
            logging.info("get_wiki_link_list search Key"+str(keyword))
            cls.collection = cls.database['wikiLinkcollection']
            linklists = cls.collection.find_one({'_id':keyword,})['links']
            for key,link in linklists.items():
                if len(output_data) >=10:
                    break
                output_data.update({key:link})
            return output_data
        except Exception as error:
            logging.error("Error occured while connecting to DB get_wiki_link_list::"+str(error))
            return False