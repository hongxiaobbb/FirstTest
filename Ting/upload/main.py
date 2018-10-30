# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 21:24:07 2018

@author: TLi5
"""

import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string
import socket
import os

DOMAIN = '.dir.slb.com'

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/upload", UploadHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

class MapHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("map.html")
        
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload_form.html")

    def post(self):
        file1 = self.request.files['file1'][0]
        original_fname = file1['filename']

        output_file = open("uploads/" + original_fname, 'wb')
        output_file.write(file1['body'])

        self.finish("file " + original_fname + " is uploaded!")
        
class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        file1 = self.request.files['file1'][0]
        original_fname = file1['filename']
        original_fname = os.path.basename(original_fname)
        output_file = open("uploads/" + original_fname, 'wb')
        output_file.write(file1['body'])
        
        head = "<html><head><title>File uploaded</title><body>"
        H = socket.gethostname()+DOMAIN
        link = "<a href=\"http://"+H+":5000/serve?filename="+original_fname+"\">Generate report</a>"
        self.finish(head+"file " + original_fname + " is uploaded.  Open the following link in a new tab: <br>"+link)
settings = {
'template_path': 'templates',
'static_path': 'static',
"xsrf_cookies": False

}
application = tornado.web.Application([
   (r"/", IndexHandler),
   (r"/map.html", MapHandler),
   (r"/upload", UploadHandler)


], debug=True,**settings)

app = application



print ("Server started.")
if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()