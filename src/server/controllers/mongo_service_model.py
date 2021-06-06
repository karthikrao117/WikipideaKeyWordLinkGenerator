import logging
from pymongo import MongoClient
import os
import bcrypt

class DBConnection:
    """
    Perform CRUD Operation on the DataBase
    """
    client = None
    collection = None
    database = None
    def __init__(self) -> None:
        pass
    
    @classmethod
    def establish_connection(cls):
        """
        establishes connection to Mongo server
        """
        try:
            cls.client = MongoClient("mongodb+srv://"+os.getenv('MONGO_USERNAME')+":"+os.getenv('MONGO_PASSWORD')+"@cluster0.i3pu3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            cls.database = cls.client['wikilink']
        except Exception as error:
            logging.error("Error occured while connecting to DB::"+str(error))
    
    @classmethod
    def db_update_wiki_collection_data(cls,keyword,keyLinkList):
        """
        updates the keyword, wikilinks data to DB
        """
        try:
            cls.collection = cls.database['wikicollection']
            cls.collection.insert({'_id':keyword,'links':keyLinkList})
        except Exception as error:
            logging.error("Error occured in DBConnection Module db_update_wiki_collection_data::"+str(error))

    @classmethod
    def wiki_link_exists(cls,keyword):
        """
        checks if a wiki link already exists
        """
        try:
            cls.collection = cls.database['wikicollection']
            if cls.collection.find({'_id':keyword}).count() > 0:
                return True
            return False
        except Exception as error:
            logging.error("Error occured in DBConnection Module wiki_link_exists::"+str(error))
            return False
    
    @classmethod
    def get_wiki_link_list(cls,keyword):
        """
        get the top 10 links for the searched keyword
        """
        output_data = {}
        try:
            cls.collection = cls.database['wikicollection']
            linklists = cls.collection.find_one({'_id':keyword,})
            if linklists:
                for key,link in linklists['links'].items():
                    if len(output_data) >=10:
                        break
                    output_data.update({key:"https://en.wikipedia.org"+link})
            return output_data
        except Exception as error:
            logging.error("Error occured in DBConnection Module get_wiki_link_list::"+str(error))
            return False
    
    @classmethod
    def auth_sign_up(cls,user_name,user_password):
        """
        Register user information
        """
        try:
            cls.collection = cls.database['userdata']
            if cls.collection.find({'user_name':user_name}).count() > 0:
                return 'User_Already_Exists'
            else:
                bpassword = user_password.encode('utf-8')
                hashed_password = bcrypt.hashpw(bpassword,bcrypt.gensalt())
                cls.collection.insert({'user_name':user_name,'user_password':hashed_password})
                return True
        except Exception as error:
            logging.error("Error occured in DBConnection Module auth_sign_up::"+str(error))
            return False
        
    @classmethod
    def auth_user_exists(cls,user_name):
        """
        Check if the authorized user exists
        """
        try:
            cls.collection = cls.database['userdata']
            if cls.collection.find({'user_name':user_name}).count() > 0:
                return True
            return False
        except Exception as error:
            logging.error("Error occured in DBConnection Module auth_user_exists::"+str(error))
            return False
        
    @classmethod
    def auth_login(cls,user_name,user_password):
        """
        Verify user credentials
        """
        try:
            cls.collection = cls.database['userdata']
            user_data = cls.collection.find_one({'user_name':user_name})
            print(user_data)
            if user_data:
                if bcrypt.checkpw(user_password.encode('utf-8'),user_data['user_password']):
                    return True
            return 'User_Do_Not_Exist'
        except Exception as error:
            logging.error("Error occured in DBConnection Module auth_login::"+str(error))
            return False