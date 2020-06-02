#!/usr/bin/env python3

import sys, getopt

import http.server
import socketserver




class HogueHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		print(self.headers)
		http.server.SimpleHTTPRequestHandler.do_GET(self)
	
	def do_HEAD(self):
		print(self.headers)
		http.server.SimpleHTTPRequestHandler.do_GET(self),





def main(argv):
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
	with socketserver.TCPServer((address,port),  HogueHandler) as httpd:
		print("serving at", address, "port", port)
		try:
			httpd.serve_forever()
		except KeyboardInterrupt:
			httpd.shutdown()

if __name__ == "__main__":
	main(sys.argv[1:])

