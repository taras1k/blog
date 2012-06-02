# -*- coding: utf-8 -*-
class Urls(object):
    """Urls helper"""
    def __init__(self):
        self.urls = {}
    
    def add(self, url, name):
        self.urls[name] = url
        
    def url_for(self, name, param=None):
        return self.urls[name] + (param if param else '')

url = Urls()

def get_page(g_page):        
    page = 0
    try:
        page = int(g_page)
    except:
        pass
    return page