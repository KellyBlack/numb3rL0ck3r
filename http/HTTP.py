#!/usr/bin/python

#
#
# Copyright (c) 2011, Kelly Black (kjblack@gmail.com)
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

from datetime import *
from datetime import timedelta


class HTTP :

    def __init__(self) :
	self.setPath("")
	self.setDomain("")

    def setPath(self,path) :
	self.path = path

    def getPath(self) :
	return(self.path)

    def setDomain(self,domain) :
	self.domain = domain

    def getDomain(self) :
	return(self.domain)

    def nextCookieExpiry(self) :
	# Figure when a cookie expires.
	#self.cookieExpires = datetime.today() +  timedelta(31)

	#week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat')
	#month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')

	#stamp = self.cookieExpires.strftime(
	#    week[int(self.cookieExpires.strftime("%w"))] + ", %d-" + \
	#    month[int(self.cookieExpires.strftime("%m"))] + "-%Y %H:%M:%S GMT")

	
	#return(stamp)
	return("Max-Age=" + str(30*24*60*60))

    def setCookie(self,name,value,retain=False) :

	cookie = "Cookie: " + name + "=" + str(value)
	if(retain) :
	    cookie += "; " + self.nextCookieExpiry()

	domain = self.getDomain()
	if(domain) :
	    cookie += "; Domain=" + domain

	path = self.getPath()
	if(path) :
	    cookie += "; Path=" + path

	print(cookie)
	return(cookie)

    def printContentType(self) :
	print("Content-Type: text/html");

    def printHeader(self,cookie=False,retain=False) :
	self.printContentType()

	if(cookie) :
	    print(self.setCookie("id","value",retain))

	print("\n");


if (__name__ == "__main__") :
    http = HTTP()
    a = http.nextCookieExpiry()
    http.setPath("/")
    http.setDomain("www.here.com")
    http.setCookie("one","two",True)
    http.printHeader()
	
	

