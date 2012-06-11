from time import time
from datetime import datetime
from dateutil.parser import parse
from models import PostModel

class Post(object):

    def __init__(self, users, post_url=None):
        self.users = users
        self.post_model = PostModel()
        self.time_format = '%Y-%m-%d %H:%M'
        if self.users.get_user():
            self.post_db = self.post_model.find_one({'post_url':post_url})
        else:
            d = datetime.today().strftime(self.time_format)
            self.post_db = self.post_model.find_one({'post_url':post_url,'$and':[{'post_drafts':False},{'post_date': {'$lt': d}}]})
        if self.post_db is None:
            self.post_db = {}     

    @property
    def post_title(self):
        if 'post_title' in self.post_db:
            return self.post_db['post_title']
        else:
            return ''
        #return ''

    @post_title.setter
    def post_title(self, value):
        self.post_db['post_title'] = value
    
    @property
    def post_body(self):
        if 'post_body' in self.post_db:
            return self.post_db['post_body']
        return ''

    @post_body.setter
    def post_body(self, value):
        self.post_db['post_body'] = value

    @property
    def post_date(self):
        if 'post_date' in self.post_db:
            return self.post_db['post_date']
        return ''

    @post_date.setter
    def post_date(self, value):
        self.post_db['post_date'] = value

    @property
    def post_drafts(self):
        if 'post_drafts' in self.post_db:
            return self.post_db['post_drafts']
        return ''

    @post_drafts.setter
    def post_drafts(self, value):
        self.post_db['post_drafts'] = value

    @property
    def post_url(self):
        if 'post_url' in self.post_db:
            return self.post_db['post_url']
        return ''

    @post_url.setter
    def post_url(self, value):
        self.post_db['post_url'] = value

    def generate_url(self):
        return str(time()).replace('.', '')

    def prepare(self):
        if 'post_url' not in self.post_db or not self.post_db['post_url']:
            self.post_db['post_url'] = self.generate_url()
        if 'post_date' not in self.post_db or not self.post_db['post_date']:
            self.post_db['post_date'] = str(datetime.today())
        if 'post_drafts' not in self.post_db or self.post_db['post_drafts'] == 'on':    
            self.post_db['post_drafts'] = True        
        self.post_db['post_date'] = parse(self.post_db['post_date']).strftime(self.time_format)

    def save(self):
        self.prepare()
        self.post_model.save(self.post_db)

    def delete(self):
        self.post_model.remove(self.post_db)


    def get_posts_count(self):
        if self.users.get_user():
            posts = self.post_model.find({})
        else:
            d = datetime.today().strftime(self.time_format)
            posts = self.post_model.find({'$and':[{'post_drafts':False},{'post_date': {'$lt': d}}]})
        return posts.count()


    def get_posts(self, skip_from=0, limit_to=5):        
        if skip_from < 0: 
            skip_from = 0
        if limit_to < 0: 
            limit_to = 10
        if self.users.get_user():
            posts = self.post_model.find({})
        else:
            d = datetime.today().strftime(self.time_format)
            posts = self.post_model.find({'$and':[{'post_drafts':False},{'post_date': {'$lt': d}}]})
        return posts.skip(skip_from).limit(limit_to)
