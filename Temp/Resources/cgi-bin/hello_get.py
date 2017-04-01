#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb
import cStringIO
from cStringIO import StringIO

# Create instance of FieldStorage 
data = 'first_name=Mohit&last_name=Jindal'
data = StringIO('first_name=Mohit&last_name=Jindal')
header = """POST /cgi-bin/hello_get.py HTTP/1.1
Host: 172.25.14.62:8888
Connection: keep-alive
Content-Length: 33
Cache-Control: max-age=0
Origin: http://172.25.14.62:8888
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"""

form = cgi.FieldStorage(fp=data, headers=header, environ={'REQUEST_METHOD':'POST'}) 

# Get data from fields
print form.list
first_name = form.getvalue('first_name')
last_name  = form.getvalue('last_name')

print "HTTP/1.1 200 OK"
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>Hello %s %s</h2>" % (first_name, last_name)
print "</body>"
print "</html>"

