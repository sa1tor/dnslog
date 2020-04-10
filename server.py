import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import sqlite3
import multiprocessing
import dnslog
import string
import random

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.set_header('Server', 'Nginx')
        self.conn = self.application.conn

class IndexHandler(BaseHandler):    
    def get(self):
        cursor = self.conn.cursor()
        sql = "select * from `log`"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.render("index.html",result=result)
    def post(self):
        get = self.get_argument('get',None)
        delete = self.get_argument('delete',None)
        if get == 'true':
            self.write(''.join(random.sample(string.lowercase+string.digits,5)))
        else:
            self.write('0')
        if delete == 'true':
            cursor = self.conn.cursor()
            sql = "delete from `log`"
            cursor.execute(sql)
            sql = "delete from sqlite_sequence where name='log'"
            cursor.execute(sql)
            cursor.execute("VACUUM")
            self.conn.commit()
            self.write('1')
        else:
            self.write('0')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
        ]
        self.conn = sqlite3.connect('./dnslog.db')
        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
            'static_path': os.path.join(os.path.dirname(__file__), "static"),
            'debug': True,
            'cookie_secret': 'ea78c248-c5d0-4dd7-9780-cdb2f40ec21e',
        }
        tornado.web.Application.__init__(self,handlers,**settings)
        
if __name__ == "__main__":
    p = multiprocessing.Process(target=dnslog.main)
    p.daemon = True
    p.start()
    tornado.options.parse_command_line()
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
