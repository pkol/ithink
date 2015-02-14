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

import threading
import collections
import time

class Snot():
	def __init__(self, maxlen=1000):
		self.q = collections.deque(maxlen = maxlen)
		self.lastId = 0
		self.cv = threading.Condition()

	def push(self, msg, attr):
		with self.cv:
			self.lastId = self.lastId + 1
			msgId = self.lastId
			self.q.append({"id": msgId, "attr": attr, "msg":msg})
			self.cv.notify_all()
			print self.q
		return msgId	

	def wait(self, lastId, attr, timeout):
		ret = []
		tend = time.time() + timeout
		with self.cv:
			while len(ret) == 0:
				for e in reversed(self.q):
					if(e["id"] > lastId):
						if e["attr"] == attr:
							print "append"
							ret.append(e);
					else:
						break
				if len(ret) == 0 and time.time() < tend:
					self.cv.wait(tend - time.time())
				else:
					ret.reverse()
					return ret

	
def testme2():
	s = Snot()



testme2()
	
