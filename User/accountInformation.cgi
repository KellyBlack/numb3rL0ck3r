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
import sys
import os
sys.path.append( os.path.join( os.getcwd(), '..' ) )

import cgi
formValues = cgi.FieldStorage()

# Enable debugging - comment this out for production! *TODO*
import cgitb
cgitb.enable()


# Get the class to deal with user management
from User.Authorize import Authorize
authorization = Authorize()



# Check to see if a user name and password form was submitted
if(('password' in formValues) and ('confirmPassword' in formValues) and ('currentPassword' in formValues)):
    # TODO - verify the password
    # TODO - verify that they match
    # TODO - save the new password
    pass

# Get the configuration information 
from config.Config import Config
localConfig = Config('../')
localConfig.parseConfigurationFile()

# Get the authorization information
authorization = Authorize(localConfig.getPassPhrase())


# get the controler to print the page
from Controller.AccountController import AccountInformation
mainControl = AccountInformation('accountInformation.tmpl',localConfig.diskOptions['templateDir'])
mainControl.renderPage(**localConfig.getConfigurationDict())

