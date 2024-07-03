#!/usr/bin/env python3
"""
This script is used to set up the environment
variables and load the configuration.
"""

# Import necessary modules and load environment variables from.env file
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
