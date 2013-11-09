#!/usr/bin/env python

import tornado.auth
import torndb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from tornado import autoreload
import os.path




# app specific settings
import urls
import uimodules.uimodules

import utils.ui_methods
from utils.settings import *

import logging


define("port", default=None, help="run on the given port", type=int)
define("port_offset", default=0, help="port - port_offset = real_port. this is helpful with supervisor")

# class Application(tornado.wsgi.WSGIApplication):
class Application(tornado.web.Application):
    def __init__(self):

        template_path = "resources/templates"
        static_path = "resources/static"
        if options.port is None:
            options.port = WWW_PORT

        handlers = urls.handlers

        settings = dict(
            title=u"Flickit",
            template_path=os.path.join(os.path.dirname(__file__), template_path),
            ui_modules=uimodules.uimodules,
            ui_methods=utils.ui_methods,
            static_path=os.path.join(os.path.dirname(__file__), static_path),
            xsrf_cookies=True,
            cookie_secret=WWW_COOKIE_SECRET,
            login_url="/login",
            autoescape=None,
            debug=DEBUG_VALUE
        )

        tornado.web.Application.__init__(self, handlers, **settings)

        # mysql
        self.mysqldb = torndb.Connection(
            host=MYSQL_DB_HOST, 
            database=MYSQL_DB_NAME,
            user=MYSQL_DB_USER, 
            password=MYSQL_DB_PASSWORD
        )


    

def main():
    from tornado.httpserver import HTTPServer 
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    real_port = options.port - options.port_offset
    http_server.listen(real_port)
    print('Listening at port %s' % real_port)
    
    ioloop = tornado.ioloop.IOLoop.instance()
    autoreload.start(ioloop)
    ioloop.start()



if __name__ == "__main__":
    main()



