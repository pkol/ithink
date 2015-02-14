#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Paweł Kołodziej <p.kolodziej@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import SocketServer
import BaseHTTPServer
import snot
import urlparse
import json

class SnotHttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):

		u= urlparse.urlparse(self.path)
		args = urlparse.parse_qs(u.query)
		self.send_response(200)
		self.end_headers()
		if u.path =='/send':
			#print "SEND!!! %s |%s|" % (self.path, args['event'][0])
			event =  json.loads(args['event'][0])
			attr =  args['attr'][0]
			eventId = self.server.snot.push(event, attr)
			ret = eventId
		elif u.path =='/get':
			#print "GET"
			lastId = int(args['lastId'][0])
			timeout = float(args['timeout'][0])
			attr = args['attr'][0]
			ret = self.server.snot.wait(lastId, attr, timeout)
		else:
			print "unknown path '%s'" %(u.path)
		#print "serialize %s" %(ret)
		json.dump(ret, self.wfile)


		return

class SnotHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
	def __init__(self, addr):
		self.snot = snot.Snot()
		self.daemon_threads = False
		BaseHTTPServer.HTTPServer.__init__(self, addr, SnotHttpHandler)
	  


SnotHTTPServer(('',1080)).serve_forever()
