import jwt
import datetime
import logging
import os

from .mongo_service_model import DBConnection

class AuthModel:
    """ AuthModel  for authentication handling """


    @classmethod
    def user_auth_signup(cls,user_name,user_password):
        try:
            token = None
            returned_data = DBConnection.auth_sign_up(user_name,user_password)
            if returned_data == 'User_Already_Exists':
                message = returned_data
                status = 'Failure'
            elif returned_data == True:
                token = AuthModel.encode_auth_token(user_name)
                if token:
                    message = 'Registartion Success'
                    status = 'Success'
                else:
                    status = 'Failure'
                    message = 'Signedup successfully'
                    token = None
            else:
                status = 'Failure'
                message = 'Failed To Sign Up'
            return {'message':message,'status':status, 'auth_token':token}
        except Exception as error:
            logging.error("Error occured in user_auth_signup"+str(error))
            return {'status':'Failure','message':'Failed To Sign Up'}

    @staticmethod
    def encode_auth_token(user_name):
        """
        Generates the Auth Token
        :param usern_name:subscriber
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3600),
                'iat': datetime.datetime.utcnow(),
                'sub': user_name
            }
            return jwt.encode(
                payload,
                os.getenv('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as error:
            logging.error("Error occured in jwt encoding"+str(error))
            return False

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, os.getenv('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            logging.error('Signature expired. Please log in again.')
            return False
        except jwt.InvalidTokenError:
            logging.error('Invalid token. Please log in again.')
            return False
        except  Exception as error:
            logging.error('Exception occured in decode_auth_token:: '+str(error))
            return False

    def verify_user_validity(auth_token):
        try:
            subscriber = AuthModel.decode_auth_token(auth_token)
            if subscriber:
                return DBConnection.auth_user_exists(subscriber)
            return False
        except  Exception as error:
            logging.error('Exception occured in verify_user_validity:: '+str(error))
            return False
            
