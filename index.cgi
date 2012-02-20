#!/usr/bin/python

#
#
# Copyright (c) 2012, Kelly Black (kjblack@gmail.com)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following
#    disclaimer.
#
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided with
#    the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
#


#import cgi

# Enable debugging - comment this out for production! *TODO*
import cgitb
cgitb.enable()

# Read in the necessary mako template classes
from mako.template import Template
from mako.lookup import TemplateLookup
templateLookup = TemplateLookup(directories=['./'])


# Get the local modules necessary for this site.
from User.Authorize import Authorize
from config.Config import Config

# Print out the http header. (Assumes everything that follows is
# printable material!)
print("Content-Type: text/html\n\n")


# Get the authorization information
authorization = Authorize()
#authorization.printCookieInformation()

# Get any necessary local information
localConfig = Config()
localConfig.parseConfigurationFile()


# get the template for the main page.

t = Template(filename='template/basePage.tmpl',lookup=templateLookup)

print(t.render(templateDir="template",
               **localConfig.getConfigurationDict()))


# Print out all the environment info
#print("<p>hello</p>")
#for key,value in os.environ.iteritems():
#    print("{0} - {1}<br>".format(key,value))

