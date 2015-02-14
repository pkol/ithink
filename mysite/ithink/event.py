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

from django.http import HttpResponse
from ithink.models import *
from operator import attrgetter
import time
import json
import urllib

SNOT_SERVER="http://localhost:1080"

#XXX fimxe - add locking
lastEventId=0

def eventAdd(data):
	global lastEventId
	lastEventId = int(urllib.urlopen("%s/send?attr=0&event=%s" %(SNOT_SERVER, urllib.quote(json.dumps(data)))).read())

def eventGetLastId():
	global lastEventId
	return lastEventId
	

def eventWait(lastId, timeout):
	s = urllib.urlopen("%s/get?lastId=%s&timeout=%s&attr=0"%(SNOT_SERVER,lastId, timeout)).read()
	ret = json.loads(s)
	ret = [{'id':x['id'], 'data':x['msg']} for x in ret]
	return ret
		
	
