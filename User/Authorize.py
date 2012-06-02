#!/usr/bin/python

#
#
# Copyright (c) 2011-2012, Kelly Black (kjblack@gmail.com)
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

# This is the class used to decide if a client is authorized to access
# the inforation requested. It keeps track of the person's access level
# and the access required for a piece of information.

# Import the modules necessary for authentication
import hmac
import hashlib

# Import the modules necessary for reading and parsing the cookies
import Cookie
import os
import re



class Authorize :
    parseUserCookie = re.compile(r'^(?P<user>.*);(?P<hash>[a-zA-Z0-9]*)')
    
    def __init__(self,passPhrase="",theHash="") :
        # Assume not logged in
        self.authorized = False
        self.username = ""

	# Set the passphrase and hash.
	self.setPassPhrase(passPhrase)
	self.setRemoteHash(theHash)


	# Get the cookies and see what we've got...
	self.haveCookies = False
	self.cookies = Cookie.SimpleCookie()
	try:
	    self.cookies.load(os.environ["HTTP_COOKIE"])
	    self.haveCookies = True
	    #print("Got cookies<br>")
	except KeyError:
	    #print("No cookies")
	    pass # Should we do something here?

        if('user' in self.cookies) :
            theUser = ''
            theHash = ''
            check = self.parseUserCookie.search(self.cookies['user'].value)
            try:
                theUser = check.group('user')
            except IndexError:
                #print("user not there")
                return

            try:
                theHash = check.group('hash')
            except IndexError:
                #print("hash not there")
                return

            self.authorized = self.checkUserHash(theUser,theHash)

    def setPassPhrase(self,value):
	self.passPhrase = value
	self.digest = hmac.new(value,'',hashlib.sha1)

    def getPassPhrase(self) :
	return(self.passPhrase)

    def resetDigest(self) :
	#print("Using passphrase: {0}".format(self.getPassPhrase()))
	self.digest = hmac.new(self.getPassPhrase(),'',hashlib.sha1)

    def setRemoteHash(self,theHash) :
	self.remoteHash = theHash

    def getHash(self,message) :
	self.resetDigest()
	self.digest.update(message)
	return(self.digest.hexdigest())

    def isAuthorized(self,message,theHash) :
	#print("New hash: {0} sent hash: {1}".format(self.getHash(message),theHash))
	return(self.getHash(message)==theHash)

    def checkUserHash(self,user,theHash):
        # TODO - get the user's hash from the datbase and compare
        # THis is the hash that comes from the cookie.
        return(True)
        

    def hmacSHA1(self,message) :
	return(False)

    def printCookieInformation(self):
	# Print out any cookies we might have.
	if(self.haveCookies):
	    print("<p>We have cookies!</p>")
	    num = 1
	    for key,value in self.cookies.iteritems():
		print("{0} - {1} - {2}<br>".format(num,key,value.value))
		num = num + 1


    def deleteCookies(self):
	# Print out any cookies we might have.
	if(self.haveCookies):
	    #print("<p>We have cookies!</p>")
	    for key,value in self.cookies.iteritems():
                print('Set-Cookie:{0}=""; Expires=Thu, 01 Jan 1970 00:00:01 GMT;'.format(key))


    def setUser(self,username,password):
	# Routine to set the user name for this person

	# TODO Need to properly set the cookie. For now just do
	# something silly until we get the cookie thing working.
        self.username = username
	self.cookies['user'] = username + ";" + "hash"
	self.cookies['user']['path']    = '/'  # TODO change the path!
	self.cookies['user']['domain']  = 'playroom.edu' # TODO change the domain!
        self.cookies['user']['expires'] = 60*60*24
	

    def checkUser(self,username,password):
	#routine to check to see if the user and password are correct
	# TODO add a check to see if the hash matches.
        self.authorized = self.checkPassword(username,password)
        if(self.authorized):
            self.setUser(username,password)
            self.printCookie()
	return(self.authorized)

    def checkPassword(self,username,password):
        return(True) # TODO - check the hash that is in the database.
        
    def printCookie(self):
	print(self.cookies.output())

    def userAuthorized(self):
        return(self.authorized)

    def getUserName(self):
        return(self.username)

if (__name__ =='__main__') :
    auth = Authorize()
    auth.setPassPhrase('123')
    theHash = auth.getHash('hello')
    print(theHash)
    print(type(theHash))
    if(auth.isAuthorized('hello',theHash)) :
	print("it is good")

    if(auth.isAuthorized('hello','bubba')) :
	print("it is horribly wrong")
    
