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

# Import the necessary parts for sending mail.
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import mimetypes

import sys
import os
sys.path.append( os.path.join( os.getcwd(), '..' ) )

import cgi
formValues = cgi.FieldStorage()

# Enable debugging - comment this out for production! *TODO*
import cgitb
#cgitb.enable()


# Get the class to deal with user management
from User.Authorize import Authorize
authorization = Authorize()

# Get the configuration information
from config.Config import Config
localConfig = Config('../')
localConfig.parseConfigurationFile()

# Get the authorization information
authorization = Authorize(localConfig.getPassPhrase())

from Controller.AccountController import LoginController,EmailController
email=""
email_confirm=""
password=""
password_confirm=""
emailMatches = True
passwordMatches = True
userExists = False
mainControl = None

# This is only for testing - delete it! *TODO*
#formValues = {'email':'kjblack@gmail.com',
#	      'email_confirm':'kjblack@gmail.com',
#	      'password':'bubba',
#	      'password_confirm':'bubba'}
# First - ask if this is about creating a new user.
if(('email' in formValues) and ('email_confirm' in formValues) and \
   ('password' in formValues) and ('password_confirm' in formValues)):
    # This is a request to create a new account.

    emailMatches = (formValues['email'] == formValues['email_confirm'])
    passwordMatches = (formValues['password'] == formValues['password_confirm'])

    if(emailMatches and passwordMatches):
	# The information is good.

	if(authorization.checkUserNameExists(formValues['password'])):
	   # This user exists. Need to print an error message.
	   userExists = True

	else:
	    # Everything checks and add it to the database.
	    formValues['password'] = authorization.getHash(formValues['password'])
	    emailDetails = localConfig.getMailConfigurationDict()	    
	    emailControl = EmailController('emailNewAccount.tmpl',localConfig.diskOptions['templateDir'])

	    # Set up the email
	    msg = MIMEMultipart()
	    msg['Subject'] = emailDetails['mailSubjectLine']
	    msg['From'] = emailDetails['mailFromAddress']
	    msg['To'] = formValues['email']
	    emailControl.renderPage()

	    # Create the text for the page
	    theMessage = emailControl.renderPage(email=formValues['email'],
						 password=formValues['password'],
						 **localConfig.getConfigurationDict())
	    msg.preamble = theMessage
	    theMessage   = MIMEText(theMessage,'plain')
	    msg.attach(theMessage)

	    # Now send it off
	    smtp = smtplib.SMTP(emailDetails['mailHost'],emailDetails['mailPort'])
	    smtp.login(emailDetails['mailUserName'],emailDetails['mailPassword'])
	    smtp.sendmail(emailDetails['mailFromAddress'],formValues['email'],msg.as_string())
	    
	    # TODO - save the information
	    mainControl = LoginController('newUser.tmpl',localConfig.diskOptions['templateDir'])

    else:
	# get the controler to print the page
	email=formValues['email']
	email_confirm=formValues['email_confirm']


    

# get the controler to print the page
from Controller.AccountController import LoginController
if(not mainControl):
    mainControl = LoginController('createAccount.tmpl',localConfig.diskOptions['templateDir'])
mainControl.renderPage(email=email,
		       email_confirm=email_confirm,
		       password=password,
		       password_confirm=password_confirm,
		       emailMatches = emailMatches,
		       passwordMatches = passwordMatches,
		       userExists=userExists,
		       **localConfig.getConfigurationDict()
		       )




