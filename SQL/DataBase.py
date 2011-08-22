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

import pgdb   # NOTE - this module does not come with python! It needs
              # to be installed separately.

import re

class DataBase :

    # Define some commonly used regular expressions here.
    leadingComma = re.compile(r"^,")    # Identifies a string with a comma in the first position
    trailingAND  = re.compile(r"AND $") # Identifies the string "AND " at the end of a line

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
	
	if(type(theItems)==str):
	    return(pgdb.escape_string(theItems))
	
	elif(type(theItems) == dict) :
	    self.escapeDictionary(theItems)

	elif(type(theItems)==list):
	    self.escapeList(theItems)

	else :
	    return(pgdb.escape_string(str(theItems)))

	return(None)


    def valuesFromDictionary(self,theDict) :
	to = ""
	values = ""
	for key,value in theDict.iteritems():
	    to += "," + key
	    values += ",'" + pgdb.escape_string(value) + "'"

	return(self.leadingComma.sub('',to),self.leadingComma.sub('',values))


    def valuesFromList(self,theList) :
	values = ""
	for value in theList:
	    values += ",'" + pgdb.escape_string(value) + "'"

	return(self.leadingComma.sub('',values))


    # Routine to form the list of items to choose from a query
    def queryVariables(self,theVariables) :
	query = ""
	for item in theVariables:
	    query += "," + item

	return(" " + self.leadingComma.sub('',query)+ " ")


    # Routine to concatenate a set of "joins" to form a single
    # string for the joins.
    def formJoin(self,firstTableName,theTables) :
	# theTables is a list:
	#[ ....., [table name to join, type (left/right/full/- leave blank to make an "inner"),
	#         [ [table 1,variable name,table 2,variabe name],[...]]], .... ]
	#

	join = firstTableName + " "
	for table in theTables:
	    #print(table)
	    if(len(table)==3) :
		if(table[1]) :
		    join += table[1] + " join "
		else :
		    join += "inner join "

		join += table[0] + " on ("
		for tableVars in table[2] :
		    if(len(tableVars) >= 4) :
			join += tableVars[0] + "." + tableVars[1] + \
				"=" + tableVars[2] + "." + tableVars[3] + " AND "

		join = self.trailingAND.sub(') ',join)
		
	return(join)


    
if (__name__ == "__main__") :

    db = DataBase()
    d = {"a":"b''","c":"'d"}
    (t,v) = db.valuesFromDictionary(d)
    #print("{0}\n{1}".format(t,v))
    #print(db.valuesFromList(["a'","'b","''c'"]))

    print(db.queryVariables(["a.1","a.2","b.4"]))

    print(db.formJoin("first",[["second","",[["first","c1","second","c2"],["first","c2","third","c3"]]],
			       ["third","RIGHT",[["first","c2","third","c4"],["third","c4","second","c2"]] ] ]))
