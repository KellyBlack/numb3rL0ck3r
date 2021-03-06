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


from ConfigParser import *
import re


# Class to parse and keep track of the configuration parameters for
# the web site.
class Config(SafeConfigParser):



    # Define some basic regular expressions for cleaning up a line
    # from the configuration file.
    clearComment     = re.compile(r"[ \t]*[^\\]{0,0}#.*$")  # Comment line
    leftOfEqualSign  = re.compile(r"[ \t]*=.*$")            # match stuff to the right of the equal sign.
    rightOfEqualSign = re.compile(r".*?=[ \t]*")            # match stuff to the left of the equal sign
    stripLeft        = re.compile(r"^[ \t]*[\"]*")          # Match white space and quotes to the left
    stripRight       = re.compile(r"[\"]*[ \t]*$")          # Match white space and quotes to the right

    DEBUG = False



    # method called when a class item is created.
    def __init__(self,directoryOffset="./",configFileName="config/config.dat") :
	# Set the list of configurable options.
	self.siteConfigurationOptions = \
	       {'documentDir'        : '/',
		'cgiDir'             : '/cgi-bin',
		'cssDir'             : '/css',
		'serverName'         : '',
		'administratorName'  : '',
		'administratorEmail' : '',
		'homeInstitutionName'        : '',
		'homeInstitutionDescription' : ''
		}

	self.diskOptions = \
		{
		 'templateDir' : '/tmp/templates',
	         'homeDir'     : '/www'
	        }

	self.databaseOptions = \
		{'regularDataBaseUser'         : '',
                 'regularDataBaseUserPassword' : '',
		 'ownerDataBase'               : '',
		 'ownerDataBasePassword'       : '',
                 'databaseName'                : '',
                 'databaseHost'                : '',
                 'databasePort'                : ''
		}

	self.mailOptions = \
		{'mailHost'           : '',
                 'mailPort'           : '',
		 'mailUserName'       : '',
		 'mailPassword'       : '',
                 'mailFromAddress'    : '',
		 'mailSubjectLine'    : '',
		}

	self.securityOptions = \
		{'administratorPassword' : '',
		 'passwordSecurityHash'  : ''
		 }

	ConfigParser.__init__(self)

	# Set the file name that is the configuration file.
	self.setConfigurationFile(directoryOffset+configFileName)


    # Return a pointer to the configuration file
    def getConfigurationDict(self) :
	return(self.siteConfigurationOptions)
    
    # Return a pointer to the database configuration file
    def getDatabaseConfigurationDict(self) :
	return(self.databaseOptions)

    # Return a pointer to the mail configuration file
    def getMailConfigurationDict(self) :
	return(self.mailOptions)
    
    # Return a pointer to the security configuration file
    def getSecurityConfigurationDict(self) :
	return(self.securityOptions)

    # Return a pointer to the disk configuration file
    def getDiskConfigurationDict(self):
	return(self.diskOptions)

    # set the configuration file name
    def setConfigurationFile(self,name) :
	self.configFileName = name

    # get the configuration file name
    def getConfigurationFile(self) :
	return(self.configFileName)

    # Get the security passphrase
    def getPassPhrase(self):
	return(self.securityOptions['passwordSecurityHash'])

    # Read the configuration file and parse the items in the file.
    def parseConfigurationFile(self) :

	correctFile = True
	
	try:
	    # Open the file to read
	    files = self.read(self.getConfigurationFile())
	except (ParsingError,NoSectionError,NoOptionError,InterpolationError,
		InterpolationDepthError,InterpolationSyntaxError,MissingSectionHeaderError),err:
	    print("Config.parseConfigurationFile - Error reading the configuration file. The configuration file was ignored.\n{0}".format(err))
	    return(False)

	if(len(files) == 0) :
	    # No files were found.
	    print("Config.parseConfigurationFile - Error reading the configuration file. The file was not found.")
	    return(False)
	
	#sections = self.sections()
	#for name in sections:
	#    print("Section: {0}".format(name))

	# Get the information from the "site" section.
	correctFile = correctFile and self.getSectionInformation(
	    'site',self.siteConfigurationOptions)

	# Get the information from the "disk" sect
	correctFile = correctFile and self.getSectionInformation(
	    'disk',self.diskOptions)

	# Get the information from the "database" section.
	correctFile = correctFile and self.getSectionInformation(
	    'database',self.databaseOptions)

	# Get the information from the "mail" section.
	correctFile = correctFile and self.getSectionInformation(
	    'mail',self.mailOptions)
	
	# Get the information from the "security" section
	correctFile = correctFile and self.getSectionInformation(
	    'security',self.securityOptions)

	#print("Values: {0}".format(self.siteConfigurationOptions))
	return(correctFile)



    # Method to get all of the relevant variables for a specific
    # section of the configuration file. The results are kept in the
    # keyword dictionary.
    def getSectionInformation(self,section,keyword) :
	readStatus = True

	if(not self.has_section(section)) :
	    # This section is missing from the configuration file.
	    print("Config.parseConfigurationFile - Error reading the configuration file. The configuration file is missing a '{0}' section.".format(section))
	    return(False)
	    
	for name,value in keyword.iteritems() :
	    # Check each name specified in the dictionary. Check to
	    # see what its value (if any) is in the config file.
	    #print("checking {0}".format(name))

	    if(self.has_option(section,name)) :
		try:
		    value = self.get(section,name)
		except InterpolationSyntaxError, err:
		    print("Config.getSectionInformation - There was an error in formatting a variable value: {0}".format(err))
		    readStatus = False
		    
		if(value) :
		    keyword[name] = value

	return(readStatus)


if (__name__ =='__main__') :
    conf = Config()
    if(conf.parseConfigurationFile()) :
	print(conf.siteConfigurationOptions)
	print(conf.databaseOptions)
	print(conf.mailOptions)
	print(conf.diskOptions)

    else:
	print("There was an error")
