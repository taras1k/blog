# -*- coding: utf-8 -*-
import os
import web
import users
import datetime
import settings 
from helpers import url, get_page
from controlers import Post
from session import MongoStore
from jinja2 import Environment,FileSystemLoader
import simplejson as json

POSTS_PER_PAGE = 5

url.add('/', 'home')
url.add('/static/', 'static')
url.add('/login/', 'login')
url.add('/logout/', 'logout')
url.add('/add_publication/', 'add_publication')
url.add('/edit_publication/', 'edit_publication')
url.add('/posts/', 'view_publication')
url.add('/api/json/','get_json_posts')


urls = ("/login/", "login",
        "/logout/", "logout",
		"/", "main",
        "/add_publication/", "add_publication",
        "/edit_publication/(.+)", "edit_publication",
        "/posts/(.+)", "view_publication",
        "/api/json/", "get_json_posts")

app = web.application(urls, globals())

session = web.session.Session(app, MongoStore(settings.db, 'sessions'))

users.session = session
users.collection = settings.db.users


def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)

    context['url'] = url
    context['users'] = users
    #jinja_env.update_template_context(context)
    return jinja_env.get_template(template_name).render(context)

class main:
    def GET(self):
        post = Post(users)
        params = web.input()
        pagination = {}
        g_page = params.get('page', 0)
        page = get_page(g_page)
        if page > 0:
            pagination['left'] = page - POSTS_PER_PAGE
        if page < post.get_posts_count() - POSTS_PER_PAGE:
            pagination['right'] = page + POSTS_PER_PAGE    
        return render_template('index.html', 
                                posts_data=post.get_posts(skip_from=page, 
                                                            limit_to=POSTS_PER_PAGE), 
                                page=page, pagination=pagination)

class get_json_posts:
    def GET(self):
        post = Post(users)
        params = web.input()
        g_page = params.get('page', 0)
        page = get_page(g_page)
        web.header('Content-Type', 'application/json')
        articles = list(post.get_posts(skip_from=page, 
                                    limit_to=POSTS_PER_PAGE))
        return json.dumps(str(articles))


class login:
    def GET(self):
        return render_template('login.html')

    def POST(self):
        post_data = web.input(username=None, password=None)
        user = users.authenticate(post_data.username, post_data.password)
        if user:
            users.login(user)
            web.redirect(url.url_for('home'))
        else:
            return render_template('login.html', data=post_data, bad_pass=True)

class logout:
    def GET(self):
        users.logout()
        web.redirect(url.url_for('home'))

class add_publication:

    @users.login_required
    def GET(self):
        return render_template('add_edit_publication.html', post={})

    @users.login_required
    def POST(self):
        post_data = web.input(post_title=None, 
                              post_body=None,
                              post_drafts=False,
                              post_date=str(datetime.datetime.today())
                              )
        post = Post(users)
        post.post_title = post_data['post_title']
        post.post_body = post_data['post_body']
        post.post_date = post_data['post_date']
        post.post_drafts = post_data['post_drafts']
        post.save()
        return render_template('view_publication.html', data=post_data)

class edit_publication:
    
    @users.login_required
    def GET(self, post_url):
        post = Post(users, post_url)
        return render_template('add_edit_publication.html', post=post, is_edit=True)
    
    @users.login_required
    def POST(self, post_url):
        post_data = web.input(post_title=None, 
                              post_body=None,
                              post_drafts=False,
                              post_date=str(datetime.datetime.today())
                              )
        post = Post(users, post_url)
        post.post_title = post_data['post_title']
        post.post_body = post_data['post_body']
        post.post_date = post_data['post_date']
        post.post_drafts = post_data['post_drafts']
        post.save()
        return render_template('view_publication.html', data=post_data)    

class view_publication:
    
    def GET(self, post_url):
        post = Post(users, post_url)
        return render_template('view_publication.html', data=post)

def notfound():
    return web.notfound(render_template('404.html'))

app.notfound = notfound
    
if __name__ == "__main__":
    app.run()

application = app.wsgifunc()