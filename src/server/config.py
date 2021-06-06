# project/server/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))



class DevelopmentConfig:
    """Development configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    ENV = 'development'

#Add separate for Production use Base class initially