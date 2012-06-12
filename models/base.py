# -*- coding: utf-8 -*-
from settings.database import db, connection
from pymongo import DESCENDING

class Model(object):

    def __init__(self, collection_name):
        self.collection = db[collection_name]

    def find(self, query):
        with connection.start_request() as request:
            return self.collection.find(query)

    def find_one(self, query):
        with connection.start_request() as request:
            return self.collection.find_one(query)

    def save(self, db_object):
        with connection.start_request() as request:
            self.collection.save(db_object)

    def remove(self, db_object):
        with connection.start_request() as request:
            self.collection.remove(db_object)

