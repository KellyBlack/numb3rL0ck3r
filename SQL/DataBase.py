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

# This is the class used to decide if a client is authorized to access
# the inforation requested.

import pgdb

class DataBase :

    def __init__(self,password="",database="",host="",user="") :
	self.setPassword(password)
	self.setDatabaseName(database)
	self.setHost(host)
	self.setUser(user)


    def setPassword(self,value):
	self.password = value

    def getPassword(self):
	return(self.password)


    def setDatabaseName(self,dbName) :
	self.databaseName = dbName

    def getDatabaseName(self) :
	return(self.databaseName)


    def setHost(self,host) :
	self.hostName = host

    def getHost(self) :
	return(self.hostName)


    def setUser(self,user):
	self.userName = user

    def getUser(self):
	return(self.userName)

    

    def connect(self) :
	self.db = pgdb.connect(user=self.getUser(),
			       password=self.getPassword(),
			       host=self.getHost(),
			       database=self.getDatabaseName()) # dsn=None

    def close(self) :
	self.db.close()


    def commit(self) :
	self.db.commit()


    def escapeDictionary(self,theDict) :
	for key, value in theDict.iteritems():
	    theDict[key] = pgdb.escape_string(value)


    def escapeList(self,theList) :
	lupe = 0
	for entry in theList:
	    theList[lupe] = pgdb.escape_string(entry)
	    lupe += 1


    def escapeItems(self,theItems) :
	
	if(type(theItems) == dict) :
	    self.escapeDictionary(theItems)

	elif(type(theItems)==list):
	    self.escapeList(theItems)

	elif(type(theItems)==str):
	    return(pgdb.escape_string(theItems))
	
	else :
	    return(pgdb.escape_string(str(theItems)))

if (__name__ == "__main__") :

    db = DataBase()
    d = {"a":"b''","c":"'d"}
    db.escapeItems(d)
    print(d)

    d = ["'a","b'","''c"]
    db.escapeItems(d)
    print(d)

    print(db.escapeItems("heas''"))
    print(db.escapeItems(1))
