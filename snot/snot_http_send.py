#!/usr/bin/python

import urllib
import json

print urllib.urlopen("http://localhost:1080/send?attr=2&event=%s"% (json.dumps([1,2,3]))).read()


