# -*- coding: utf-8 -*-
from settings import db, connection
from pymongo import DESCENDING

class PostModel(object):

    def __init__(self):
        self.posts = db.posts

    def find(self, query):
        with connection.start_request() as request:
            return self.posts.find(query).sort('post_date', DESCENDING)

    def find_one(self, query):
        with connection.start_request() as request:
            return self.posts.find_one(query)

    def save(self, post_db):
        with connection.start_request() as request:
            self.posts.save(post_db)

    def remove(self, post_db):
        with connection.start_request() as request:
            self.posts.remove(post_db)

