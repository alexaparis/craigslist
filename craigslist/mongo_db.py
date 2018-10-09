"""
Connection to our mongo db server
"""

import json
import logging
import os

import pymongo

class MongoConnection():
    def __init__(self):
        self.config_file = 'src/config.json'
        self.connection = None
        self.uri = self.load_config()
        self.connect()

    def load_config(self):
        logging.debug('Checking if {} exists'.format(self.config_file))
        if os.path.exists(self.config_file):
            logging.debug('Reading file {}'.format(self.config_file))
            raw_data = open(self.config_file, 'r')
            self.data = json.loads(raw_data.read())
            self.url = self.data['mongo-db']['url']
            self.users = self.data['mongo-db']['users']
            if self.users:
                self.login_user = self.users[0]['name']
                self.pass_user = self.users[0]['password']
                logging.debug('Using config data url=[{}]'.format(self.url.format(self.login_user, '*****')))
                return self.url.format(self.login_user, self.pass_user)
            msg = 'users field is not configured properly in {}'.format(self.config_file)
            logging.error(msg)
            raise ValueError(msg)
        else:
            msg = 'File {} is missing from the directory.'.format(self.config_file)
            logging.error(msg)
            raise IOError(msg)
    
    def connect(self):
        if self.connection:
            return self.connection
        try:
            self.connection = pymongo.MongoClient(self.uri)
        except Exception as e:
            print(type(e), e)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(filename)s] [%(funcName)s] [%(levelname)s] %(message)s')
    m = MongoConnection()
