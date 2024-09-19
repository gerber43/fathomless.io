#!/usr/bin/python 
import cgi 
data = cgi.FieldStorage() 
make = data.getvalue("make") 
model = data.getvalue("model") 
print ('Content-type:text/html\n\n') 
print ('<!DOCTYPE HTML>') 
print ('<html lang="en">') 
print ('<head>') 
print ('<meta charset="UTF-8">') 
print ('<title>Python Response</title>') 
print ('</head>') 
print ('<body>') 
print ('<h1>') 
for i in range(10):
  print(i);


print ('</h1>') 
print ('<a href="/get.html">back</a>') 
print ('</body>') 
print ('</html>') 