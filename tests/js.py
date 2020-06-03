#filename=js.py
#
#
# Copyright Gremwell,2020
# Author: Raf Somers
# License: GNU General Public License, version 3
#
#	Initial test to run, will check for HTTP 302 support
#




from tests import base

class HogueTestJavascript(base.HogueTest):
	def __init__(self):
		self.title = "Javascript Support"
		self.description = "Checking wether the client supports JavaScript via window.location.href entry"
		base.HogueTest.__init__(self)
	
	def send_http_response(self,handler):
		self.status="PROGRESS"
		redirurl = "/hogue/do?result="+self.id
		html="""
			<!DOCTYPE html>
			<html lang="en">
			<head>
				<meta charset="utf-8">
				<title>Hogue FTW</title>
			</head>
			<body>
				Hi there.
				<script language="JavaScript">
					window.location.href = '%s';
				</script>
			</body>
		""" % redirurl
		handler.send_response(200)
		handler.send_header('Content-type','text/html')
		handler.end_headers()
		handler.wfile.write(html.encode())


