from pymongo import MongoClient
import os

class DBConnection:
    """
    Establish connection update later
    """
    client = None
    
    def __init__(self) -> None:
        pass

    @classmethod
    def establish_connection(cls):

        cls.client = MongoClient("mongodb+srv://"+os.getenv('MONGO_USERNAME')+":"+os.getenv('MONGO_PASSWORD')+"@cluster0.i3pu3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    @classmethod
    def db_instance_provider(cls):
        db = cls.client.wikilink
        collection = db['example']
        doc1 = {"name": "Ram", "nya": [1,2,3,2,5,5]}
        collection.insert(doc1)
        return collection