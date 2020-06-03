#filename=base.py
#
#
# Copyright Gremwell,2020
# Author: Raf Somers
# License: GNU General Public License, version 3
#
#	Base class used by tests classes.
#	Each service class you implement should inherit this class.
#


import uuid


class HogueTest():
	def __init__(self):
		self.id=str(uuid.uuid4())
		self.status="TODO"
	
	def build_headers(self):
		headers={}
		return headers
	
	def build_body(self):
		body=""
		return body
	
	def run(self, handler):
		self.status="PROGRESS"
		self.prettyprint("BOLD", "Test # %s" % (self.title))
		self.prettyprint("", "Redirect client to %s" % (handler.base_uri  + 'hogue/do?test=' + self.id))
		
		#Try automed redirect to the test:
		handler.send_response(302)
		handler.send_header('Location','/hogue/do?test=' + self.id)
		handler.end_headers()
	
	def send_http_response(self,handler):
		pass
	
	def finish(self,result):
		self.status = result
		if result=="SUCCESS":
			self.prettyprint("GREEN", "[+] '%s' was succesful\n" % self.title)
		elif result =="FAILED":
			self.prettyprint("RED", "[+] '%s' failed\n" % self.title)
	
	def prettyprint(self, color_, text):
		colors={
			"NONE": "",
			"PURPLE": "\033[95m",
			"CYAN": "\033[96m",
			"DARKCYAN": "\033[36m",
			"BLUE": "\033[94m",
			"GREEN": "\033[92m",
			"YELLOW": "\033[93m",
			"RED": "\033[91m",
			"BOLD": "\033[1m",
			"UNDERLINE": "\033[4m",
			"END": "\033[0m"
		}
		if color_ is not "":
			print(colors[color_] + text + colors["END"])
		else:
			print(text)


