#!/usr/bin/python2 
import sys
import cgi #https://docs.python.org/2/library/cgi.html
print ('Content-type:text/html\n') 
HTTP_FIELDS = cgi.FieldStorage() 
if (HTTP_FIELDS.getvalue("getMap")):
  f = open("../json/map.json", "r").read()
  sys.stdout.write(f)
