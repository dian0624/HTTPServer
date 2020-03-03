# coding=utf-8
from socket import *
from threading import Thread
import os,sys
import traceback

class HTTPServer(object):
	def __init__(self,server_addr,static_dir):	 
		self.addr = server_addr
		self.dir = static_dir
		self.ip = server_addr[0]
		self.port = server_addr[1]
		self.create_socket()

	def create_socket(self):
		self.sockfd = socket()
		self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		self.sockfd.bind(self.addr)

	def serve_forever(self):
		self.sockfd.listen(5)
		print("Listen the port %d"%self.port)
		while True:
			try:
				connfd,addr = self.sockfd.accept()
			except KeyboardInterrupt:
				self.sockfd.close()
				sys.exit('服務器退出')
			except Exception :
				traceback.print_exc()
				continue
			clientThread = Thread\
			(target = self.handleRequest,args =(connfd,))
			clientThread.setDaemon(True)
			clientThread.start()

	def handleRequest(self,connfd):
		request = connfd.recv(4096)
		requestHeaders = request.splitlines()
		print(connfd.getpeername(),":",requestHeaders[0])

		getRequest = str(requestHeaders[0]).split(' ')[1]
		if getRequest == '/' or getRequest[-5:] == '.html': 
			self.get_html(connfd,getRequest)
		else:
			self.get_data(connfd,getRequest)
		connfd.close()

	def get_html(self,connfd,getRequest):
		if getRequest == '/':
			file_name = self.dir +'/index.html'
		else:
			file_name =  self.dir + getRequest

		try:
			f = open(file_name)
		except Exception:
			responseHeaders = 'HTTP/1.1 404 not found\r\n'
			responseHeaders += '\r\n'
			responseBody = "Sorry,not found the page"
		else:
			responseHeaders = 'HTTP/1.1 200 ok\r\n'
			responseHeaders += '\r\n'
			responseBody = f.read()
		finally:
			response = responseHeaders + responseBody
			connfd.send(response.encode())

	def get_data(self,connfd,getRequest):
		urls =['/time','/tedu','/python']

		if getRequest in urls:
			responseHeaders = 'HTTP/1.1 404 not found\r\n'
			responseHeaders += '\r\n'		
			if getRequest == '/time':
				import time
				responseBody = time.ctime()
			elif getRequest == '/tedu':
				responseBody = 'Welcome to tedu'
			elif getRequest == '/python':
				responseBody = "人生苦短1111"
		else:
			responseHeaders = 'HTTP/1.1 404 not found\r\n'
			responseHeaders += '\r\n'
			responseBody = "Sorry,not found the data"
		response = responseHeaders + responseBody
		connfd.send(response.encode())

if __name__ == '__main__':
	server_addr = ('0.0.0.0',8888)
	static_dir = './static'
	httpd = HTTPServer(server_addr,static_dir)
	httpd.serve_forever()
