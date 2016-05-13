"""
CS1951A Final Project
Brown University
Spring 2016

JJ, Chaitu, Vann, Steffani

Config
"""

"""
These classes are used in configuring the redis database which we are no longer using.
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
