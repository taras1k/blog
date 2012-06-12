# -*- coding: utf-8 -*-
import web
import hashlib
from settings.database import connection
import sensetive_info 

SALTY_GOODNESS = sensetive_info.SALTY_GOODNESS

#Must be set by the thing importing this module
collection = None
session = None

def get_user():

    try:
        u = collection.find_one({'_id':session._user_id}) 
        return u
    except AttributeError:
        return None

def authenticate(username, password):
    with connection.start_request() as request:
        user = collection.find_one({'username':username, 'password':pswd(password)})
        return user if user else None

def login(user):
    session._user_id = user['_id']
    return user

def logout():
    session.kill()

def register(**kwargs):
    with connection.start_request() as request:
        user = collection.save(kwargs)
        return user
    
def pswd(password):
    seasoned = password + SALTY_GOODNESS
    seasoned = seasoned.encode('utf-8')
    return hashlib.md5(seasoned).hexdigest()

def login_required(function, login_page='/login'):
    def inner(*args, **kwargs):
        if get_user():
            return function(*args, **kwargs)
        else:
            return web.seeother(login_page+'?next=%s' % web.ctx.get('path','/'))
    return inner
