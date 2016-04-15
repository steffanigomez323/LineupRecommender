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
    REDIS_HOST = 'aws-us-east-1-portal.9.dblayer.com'
    REDIS_PASSWORD = 'IVXUMLRMMGGGXNDC'
    REDIS_PORT = 10876


class ProductionConfig(BaseConfig):
    DEBUG = False
    REDIS_HOST = 'aws-us-east-1-portal.9.dblayer.com'
    REDIS_PASSWORD = 'IVXUMLRMMGGGXNDC'
    REDIS_PORT = 10876
