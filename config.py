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
    REDIS_HOST = 'aws-us-east-1-portal.4.dblayer.com'
    REDIS_PASSWORD = 'BWJXVIZXCPLORQLA'
    REDIS_PORT = 11333

class ProductionConfig(BaseConfig):
    DEBUG = False
    REDIS_HOST = 'aws-us-east-1-portal.4.dblayer.com'
    REDIS_PASSWORD = 'BWJXVIZXCPLORQLA'
    REDIS_PORT = 11333
