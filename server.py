#  coding: utf-8 
import socketserver
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.data=self.data.decode("utf-8")
        request=self.data.split('\n')[0]
      
        # If not GET request
        if not request.startswith('GET'):
            self.request.send(b'HTTP/1.0 405 Method Not Allowed\r\n')
        else:
            # check if path exists
            # make the path for a GET request
            main_directory=os.path.abspath("www")
            path=main_directory+request.split()[1]    
            if(os.path.exists(path)):
                if path.endswith('html'):
                    self.render_files('html',path)
                elif path.endswith('css'):
                    self.render_files('css',path)
                elif path.endswith('/'):
                     self.render_files('html', path+'/index.html')
                elif "/.." in path:
                    self.request.send(b'HTTP/1.0 404 Not Found\r\n')
                    self.request.send(b'\r\n')
                else:
                    location='location : {}'.format('http://127.0.0.1:8080'+request+'/')
                    self.request.send(b'HTTP/1.0 301 Moved Permanently\r\n')
                    self.request.send(b'Content-Type: text/html\n')
                    self.request.send(bytearray(location,'utf-8'))
                    self.request.send(b'\r\n')
            else:
                self.request.send(b'HTTP/1.0 404 Not Found\r\n')
                self.request.send(b'\r\n')
            
    # render files 
    def render_files(self,request_type,path):
        file_response=open(path).read()
        if request_type=='css':
            mimetype='text/css'
        if request_type=='html':
            mimetype='text/html'
        self.request.send(b'HTTP/1.0 200 OK\n') 
        self.request.send(bytearray('Content-Type: {} \n'.format(mimetype),'utf-8'))
        self.request.send(b'\n')
        self.request.send(bytearray(file_response,'utf-8'))
    
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
