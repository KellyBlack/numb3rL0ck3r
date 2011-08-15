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


import re


# Class to parse and keep track of the configuration parameters for
# the web site.
class Config :



    # Define some basic regular expressions for cleaning up a line
    # from the configuration file.
    clearComment     = re.compile(r"[ \t]*[^\\]{0,0}#.*$")  # Comment line
    leftOfEqualSign  = re.compile(r"[ \t]*=.*$")            # match stuff to the right of the equal sign.
    rightOfEqualSign = re.compile(r".*?=[ \t]*")            # match stuff to the left of the equal sign
    stripLeft        = re.compile(r"^[ \t]*[\"]*")          # Match white space and quotes to the left
    stripRight       = re.compile(r"[\"]*[ \t]*$")          # Match white space and quotes to the right

    DEBUG = False



    # method called when a class item is created.
    def __init__(self,configFileName="config/config.dat") :

	# Set the file name that is the configuration file.
	self.configFileName = configFileName

	# Set the list of configurable options.
	self.configurationOptions = \
	       {'documentDir'        : '/',
		'cgiDir'             : '/cgi-bin',
		'cssDir'             : '/css',
		'administratorName'  : '',
		'administratorEmail' : ''
		}


    # Return a pointer to the configuration file
    def getConfigurationDict(self) :
	return(self.configurationOptions)


    # Read the configuration file and parse the items in the file.
    def parseConfigurationFile(self) :

	try:
	    fp = open(self.configFileName,"r")

	except IOError:
	    # *TODO* make an error log here
	    return(False)

	# The file exists. Read each line and parse the line.
	for row in fp:
	    row = Config.clearComment.sub('',row).rstrip()   # Get rid of comments.
	    
	    if(len(row)>0) :
		# This is a non empty row. Split up the left and right
		# sides which are separated by an "equal sign."
		left  = Config.leftOfEqualSign.sub('',row)
		right = Config.rightOfEqualSign.sub('',row)
		right = Config.stripRight.sub('',right)
		right = Config.stripLeft.sub('',right)

		if(left in self.configurationOptions) :
		    # This is a valid option.
		    self.configurationOptions[left] = right

		if(self.DEBUG) :
		    print("Line: {0} - {1}/{2}".format(row,left,right))


	print(self.configurationOptions)


if (__name__ =='__main__') :
    conf = Config()
    conf.parseConfigurationFile()
