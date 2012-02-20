#!/usr/bin/python
import cgi
import os

import cgitb
cgitb.enable()

from User.Authorize import Authorize

# Print out the http header. (Assumes everything that follows is
# printable material!)
print("Content-Type: text/html\n\n")


# Get the authorization information
authorization = Authorize()
authorization.printCookieInformation()

# Print out all the environment info
print("<p>hello</p>")
for key,value in os.environ.iteritems():
    print("{0} - {1}<br>".format(key,value))

