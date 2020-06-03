#filename=redir.py
#
#
# Copyright Gremwell,2020
# Author: Raf Somers
# License: GNU General Public License, version 3
#
#	Checks for FTP support
#




from tests import base
import socket
import random
from threading import Timer


class HogueTestProtocol(base.HogueTest):
	def __init__(self,protocol):
		self.protocol = protocol
		self.title = "Protocol Support:" + protocol
		self.description = "Checking wether the client supports " + protocol.lower() + ":// style URLs"
		self.protocolport = random.randint(1025, 65535)
		base.HogueTest.__init__(self)
	
	def send_exploit(self,handler):
		pass

	
	def run(self, handler):
		targeturi= self.protocol + "://" + handler.address + ":" + str(self.protocolport) + "/"
		self.prettyprint("BOLD", "Test # %s" % (self.title))
		self.prettyprint("", "Redirect client to %s within 10 seconds." % targeturi)
		self.status="PROGRESS"
		#set up protocol socket, timeout after 10 seconds
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.settimeout(10)
			s.bind((handler.address, self.protocolport))
			s.listen(1)
			try:
				conn, addr = s.accept()
				if conn:
					self.finish("SUCCESS")
				else:
					self.finish("FAILED")
			except socket.timeout:
				self.finish("FAILED")
			s.close()
