#!/usr/bin/python3
import cherrypy
# from cherrypy import Tool
import os

import database as db
import admin as saadmin
import template as tmpl

import authenticate as sa
import html_functions as hf

# db.connect()
db_usermanager = db.ClassDBUserManagement()
db_usermanager.dbadmin_connect()

PATH = os.path.abspath(os.path.dirname(__file__))
print("### Path: " + PATH)

conf = {
    '/img': {
        'tools.staticdir.dir': PATH+'/img',
        'tools.staticdir.on': True,
    },
    '/favicon.ico': {
        'tools.staticfile.filename': PATH + '/img/favicon.ico',
        'tools.staticfile.on': True,
    }

}

class Root(object): pass

class AuthServerMain(object):
    @cherrypy.expose
    def index(self):
        return "Main Index Page"

    @cherrypy.expose
    def test01(self):
        return "Test URL 01"

    @cherrypy.expose
    def login(self):
        RET = hf.start() + hf.headers() + hf.style() + sa.login()
        return RET

    @cherrypy.expose
    def authenticate(self, password, remember, email):
        RET = hf.start() + hf.headers() + hf.style() + sa.auth() + "<pre>User: " + email + " Pass: " + password + " Remember: " + remember + "</pre>"
        return RET

if __name__ == '__main__':
    cherrypy.quickstart(AuthServerMain(), '/', conf)

