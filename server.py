#!/usr/bin/env python
#-*- coding: utf-8 -*-
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from ssms import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(8888)
IOLoop.instance().start()   
