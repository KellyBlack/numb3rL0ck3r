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


# script to initialize the sql used to create the initial database.

import sys
import os
sys.path.append( os.path.join( os.getcwd(), '..' ) )

# Make template classes
from mako.template import Template
from mako.lookup import TemplateLookup
templateLookup = TemplateLookup(directories=['./'])

#local classes for Numb3r L0ck3r
from config.Config import Config

# The database class. Used to escape some sensitive information.
from DataBase import DataBase

# The authorization class to get the password hash for the admin user
from User.Authorize import Authorize



# Create objects from the configuration and database classes
config = Config('../config/config.dat')

# Parse the config file.
if(config.parseConfigurationFile()) :
    # The config file was successfully parsed.
    db = DataBase()                                      # Create the db object
    siteInfo     = config.getConfigurationDict()         # Get the site variables
    databaseInfo = config.getDatabaseConfigurationDict() # get the db variables
    securityInfo = config.getSecurityConfigurationDict() # get the security variables
    siteInfo.update(databaseInfo)                        # Add all the dicts into one master
    siteInfo.update(securityInfo)

    # Set the admin password
    auth = Authorize()
    auth.setPassPhrase(securityInfo['passwordSecurityHash'])
    siteInfo['adminPassword'] = auth.getHash(securityInfo['administratorPassword'])

    # read in the create.sql template.
    sqlCreateTemplate = Template(filename='create.sql.template',lookup=templateLookup)

    # Escape the passwords to avoid any potentially embarassing sql
    # problems. Then create the new create.sql text.
    #db.escapeDictionary(siteInfo)
    siteInfo['regularDataBaseUserPassword'] = db.escapeItems(
        siteInfo['regularDataBaseUserPassword']);
    siteInfo['ownerDataBasePassword'] = db.escapeItems(
        siteInfo['ownerDataBasePassword']);

    siteInfo['homeInstitutionName'] = db.escapeItems(
        siteInfo['homeInstitutionName']);

    siteInfo['homeInstitutionDescription'] = db.escapeItems(
        siteInfo['homeInstitutionDescription']);

    siteInfo['adminPassword'] = db.escapeItems(
        siteInfo['adminPassword']);

    siteInfo['administratorEmail'] = db.escapeItems(
        siteInfo['administratorEmail']);


    # Write the text to a file.
    fp = open("create.sql","w")
    fp.write(str(sqlCreateTemplate.render(**siteInfo)))
    fp.close()

    # Now create the template for creating the database
    sqlShellCreateDB = Template(filename="create.sh.template",lookup=templateLookup)
    dataBaseCreateCommand = str(sqlShellCreateDB.render(**siteInfo))

    # Write it to a file amd notify the person about what to do:
    fp = open("create.sh","w")
    fp.write(dataBaseCreateCommand)
    fp.close()


    # Write out the instructions to the operator
    instructions = Template(filename="instructions.template",lookup=templateLookup)
    print(instructions.render(**siteInfo))
    

else :
    print("There was an error reading the configuration file.\n" +
	  "The SQL script was not created.")
