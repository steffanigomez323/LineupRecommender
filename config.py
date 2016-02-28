"""
CS1951A Final Project
Brown University
Spring 2016

JJ, Chaitu, Vann, Steffani

Config
"""


class BaseConfig(object):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    REDIS_HOST = 'aws-us-east-1-portal.6.dblayer.com'
    REDIS_PASSWORD = 'RYABQWHKVGXBKGUR'
    REDIS_PORT = 11509


class ProductionConfig(BaseConfig):
    DEBUG = False
    REDIS_HOST = 'aws-us-east-1-portal.6.dblayer.com'
    REDIS_PASSWORD = 'RYABQWHKVGXBKGUR'
    REDIS_PORT = 11509
