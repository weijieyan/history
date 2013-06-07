#!/usr/bin/env python
# encoding: utf-8
import umysql
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.database
from handlers.admin import admin_urls
from handlers.handler  import handler_urls

from tornado.options import define, options

define("port", default=8080, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="role_model", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="123000", help="blog database password")
class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            blog_title=u"Tornado Blog",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
#            ui_modules={"Entry": EntryModule},
#            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
#            autoescape=None,
#            debug=True,

        )

        handlers =[(r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, \
                    dict(path=settings['static_path'])),]+admin_urls+handler_urls
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)
#        cnn= umysql.Connection()
#        cnn.connect(config.DB_HOST, config.DB_PORT, config.DB_USER, config.DB_PASSWD, config.DB_DB,config.AUTOCOMMIT)
#        print cnn.is_connected()
#        self.db =cnn


def main():
    options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
