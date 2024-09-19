#!/usr/bin/python2 
print ('Content-type:text/html\n\n') 
import cgi #https://docs.python.org/3/library/cgi.html
HTTP_FIELDS = cgi.FieldStorage() 
#DO NOT EDIT ABOVE TEXT

#How to get http request variables
#https://fathomless.io/?test=testValue
#test = HTTP_FIELDS.getvalue("test") -> test = "testValue"

#indents are two spaces
for i in range(10):
  print(i)


#output of document can be viewed at https://fathomless.io/cgi-bin/test.cgi
