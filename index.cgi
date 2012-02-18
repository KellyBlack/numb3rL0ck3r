#!/usr/bin/python
import cgi
import Cookie
import os

import cgitb
cgitb.enable()

# Print out the http header. (Assumes everything that follows is
# printable material!)
print("Content-Type: text/html\n\n")

# Check for cookies
haveCookies = False
cookies = Cookie.Cookie()
try:
    cookies.load(os.environ["HTTP_COOKIE"])
    haveCookies = True
    print("Got cookies<br>")
except KeyError:
    print("No cookies")

# Print out all the environment info
print("<p>hello</p>")
for key,value in os.environ.iteritems():
    print("{0} - {1}<br>".format(key,value))

# Print out any cookies we might have.
if(haveCookies):
    print("<p>We have cookies!</p>")
    num = 1
    for key,value in cookies.iteritems():
	print("{0} - {1} - {2}<br>".format(num,key,value))
	num = num + 1

