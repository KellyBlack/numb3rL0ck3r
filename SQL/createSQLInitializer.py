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


# script to initialize the sql used to create the initial database.

import sys
import os
sys.path.append( os.path.join( os.getcwd(), '..' ) )

# Cheetah template classes
from Cheetah.Template import Template


#local classes for Numb3r L0ck3r
from config.Config import Config

# The database class. Used to escape some sensitive information.
from DataBase import DataBase

config = Config('../config/config.dat')
db = DataBase()

if(config.parseConfigurationFile()) :
    # The config file was successfully parsed.
    databaseInfo = config.getDatabaseConfigurationDict()

    fp = open("create.sql.template","r")
    page = ""
    for row in fp:
	page += row

    db.escapeDictionary(databaseInfo)
    template = Template(page,searchList=databaseInfo)
    print(template)

else :
    print("There was an error reading the configuration file.\n" +
	  "The SQL script was not created.")
