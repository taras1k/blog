# -*- coding: utf-8 -*-
from pymongo import Connection

connection = Connection(auto_start_request=False)
db = connection.blog