from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_config_file, options

from day05.app.myapp import *


app = Application(handlers=[
    ('/', IndexHandler),
    ('/login', LoginHandler),
    ('/sucess', SucessHandler),
    ('/register',RegisterHandler),
    ('/check',CheckHandler),
    ('/checkpass',CheckPassHandler),
    ('/checkimg',CheckImgHandler),],
    template_path='template',
    static_path='mystatics',
    ui_modules={'loginmodule': LoginModule,'blogmodule':BlogMoudle,'registermodule':RegisterModule},
    autoescape=None,)

define('login', type=int, default=9999)
parse_config_file('../config/config')

server = HTTPServer(app)
server.listen(options.login)
IOLoop.current().start()
