#!/usr/bin/env python3

import sys, getopt

import http.server
import socketserver

from tests import redir,js, protocols

BASE_PATH = "hogue/"
BASE_URI= "http://127.0.0.1:80/"
TESTS=[]



class HogueHandler(http.server.SimpleHTTPRequestHandler):
	base_uri=""
	address=""
	port=""
	def do_GET(self):
		"""
		Handles incomming get requests.
		First checks if BASE_PATH is in the request URL, returns 404 if none is found.
		If BASE_PATH IS found will hand of processing to self.handle_uri()
		"""
		if BASE_PATH in self.path:
			self.address= self.server.server_address[0]
			if "Host" in self.headers:
				self.address = self.headers["Host"].strip()
				self.address = self.address.split(":")[0]
			self.port= self.server.server_address[1]
			self.base_uri = "http://" + self.address + ":" + str(self.port) + "/"
			self.handle_uri()
		else:
			self.send_response(404)
	
	def do_HEAD(self):
		"""
		Handles incomming HEAD requests., simply returns a 200 OK
		"""
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.send_header('Content-length', 0)
		self.end_headers()
	
	def log_message(self, format, *args):
		"""Overwriting SimpleHTTPRequestHandler's 'log_message()'  to surpress superflouous messages printed to console."""
		pass
	
	def mark_old_tests_failed(self,currenttest):
		"""
			This function is called when we receive an inbound test request, it will mark all others still in progress as failed.
			They can only be in progress if we never received a result request for them, so they fail.
		"""
		for test in TESTS:
			if test.id != currenttest.id and test.status=="PROGRESS":
				test.finish("FAILED")
	
	def handle_uri(self):
		"""
		Checks for URL parmaters 'test' or 'result' to determine it needs to execute a test or benchmark a result.
		If neither is found it will attempt automated testing by checking if there are tests in TODO status and if so redirect to the first it finds.
		"""
		
		#check what request we are receiving, test, or result
		if self.path:
			parts=self.path.split("?",2)
			if len(parts)==2:
				params=parts[1].split("&")
				for param in params:
					name,value=param.split("=",2)
					if name.lower()=="test":
						#execute the requested test
						for test in TESTS:
							if test.id==value:
								self.mark_old_tests_failed(test)
								#incomming HTTP born test, build http response
								test.send_http_response(self)
								break
					elif name.lower()=="result":
						#mark test as succesfull
						for test in TESTS:
							if test.id==value and test.status=="PROGRESS":
								test.finish("SUCCESS")
								return
			else:
				# Client likely arrived at base URL
				# Check if we need to run another test, return 404 if we don't and shutdown
				nexttest=None
				for test in TESTS:
					if test.status=="TODO":
						nexttest=test
						self.mark_old_tests_failed(test)
						test.run(self)
						break 
				if nexttest is None: #No more tests, finish
					self.send_response(200)
					sys.exit()
		else:
			self.send_response(404)


def load_tests():
	"""
		Fills up global array TESTS
		If you want to add tests, create a new file with class in ./tests' which inherits the base class (see base.py) 
		and add a line here ot add class instance to TESTS array.
		Don't forget to add the class to imports at top of this file.		
	"""
	TESTS.append(redir.HogueTestRedir(302))
	TESTS.append(redir.HogueTestRedir(301))
	TESTS.append(js.HogueTestJavascript())
	TESTS.append(protocols.HogueTestProtocol("ftp"))
	TESTS.append(protocols.HogueTestProtocol("telnet"))
	TESTS.append(protocols.HogueTestProtocol("feed"))

def main(argv):
	"""
		Parse command line arguments and start web server.
		Accepted arguments:
		-p, --port 	Port to listen on, defaults to port 80
		-l --listenon	Address to lsiten on, defaults to 0.0.0.0 (all interfaces)
	"""
	port = 80
	address = "0.0.0.0"
	try:
		opts, args = getopt.getopt(argv,"p:l:",["port=","listenon="])
		for opt, arg in opts:
			if opt in ["-p","--port"]:
				port = int(arg)
			elif opt in ["-l","--listen"]:
				address = arg
	except getopt.GetoptError:
		print ('hogue.py -p <port> -l <address>')
		sys.exit(2)
	
	#start up webserver
	BASE_URI = "http://" + address + ":" + str(port) + "/"
	with socketserver.TCPServer((address,port),  HogueHandler) as httpd:
		print("\033[1mStarting server, point client towards " + BASE_URI + "hogue/ to start.\033[0m")
		load_tests()
		try:
			httpd.serve_forever()
		except KeyboardInterrupt:
			print("\n")
			httpd.shutdown()

if __name__ == "__main__":
	main(sys.argv[1:])

