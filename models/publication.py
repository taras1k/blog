from base import Model
from pymongo import DESCENDING

class PostModel(Model):

    def __init__(self):
        super(PostModel, self).__init__('posts')

    def find(self, query):
            return super(PostModel, self).find(query).sort('post_date', DESCENDING)

