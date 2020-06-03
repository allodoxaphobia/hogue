#filename=redir.py
#
#
# Copyright Gremwell,2020
# Author: Raf Somers
# License: GNU General Public License, version 3
#
#	Initial test to run, will check for HTTP 302 support
#




from tests import base

class HogueTestRedir(base.HogueTest):
	def __init__(self, code):
		self.code = str(code)
		self.title = "HTTP "+ self.code +" Redirection Test"
		self.description = "Checking wether the client supports HTTP "+ self.code + " redirects. This test should always be run first"
		base.HogueTest.__init__(self)
	
	def send_http_response(self,handler):
		self.status="PROGRESS"
		handler.send_response(302)
		handler.send_header('Location','/hogue/do?result='+self.id)
		handler.end_headers()

