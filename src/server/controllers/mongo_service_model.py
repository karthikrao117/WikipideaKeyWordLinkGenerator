import logging
from pymongo import MongoClient
import os
import bcrypt

class DBConnection:
    """
    Establish connection update later
    """
    client = None
    collection = None
    database = None
    def __init__(self) -> None:
        pass
    
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
            cls.collection = cls.database['wikicollection']
            cls.collection.insert({'_id':keyword,'links':keyLinkList})
        except Exception as error:
            logging.error("Error occured while connecting to DB db_update_collection_data::"+str(error))

    @classmethod
    def wiki_link_exists(cls,keyword):
        try:
            logging.info("wiki_link_exists search Key"+str(keyword))
            cls.collection = cls.database['wikicollection']
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
            cls.collection = cls.database['wikicollection']
            linklists = cls.collection.find_one({'_id':keyword,})
            if linklists:
                for key,link in linklists['links'].items():
                    if len(output_data) >=10:
                        break
                    output_data.update({key:"https://en.wikipedia.org"+link})
            return output_data
        except Exception as error:
            logging.error("Error occured while connecting to DB get_wiki_link_list::"+str(error))
            return False
    
    @classmethod
    def auth_sign_up(cls,user_name,user_password):
        try:
            cls.collection = cls.database['userdata']
            if cls.collection.find({'user_name':user_name}).count() > 0:
                return 'User_Already_Exists'
            else:
                bpassword = user_password.encode('utf-8')
                hashed_password = bcrypt.hashpw(bpassword,bcrypt.gensalt())
                cls.collection.insert({'user_name':user_name,'password':hashed_password})
                return True
        except Exception as error:
            logging.error("Error occured while connecting to DB auth_sign_up::"+str(error))
            return False
        
    @classmethod
    def auth_user_exists(cls,user_name):
        try:
            cls.collection = cls.database['userdata']
            if cls.collection.find_one({'user_name':user_name}).count() > 0:
                return True
            return False
        except Exception as error:
            logging.error("Error occured while connecting to DB wiki_link_exists::"+str(error))
            return False