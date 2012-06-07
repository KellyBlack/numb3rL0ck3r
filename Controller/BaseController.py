#!/usr/bin/python

#
#
# Copyright (c) 2012, Kelly Black (kjblack@gmail.com)
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

from mako.template import Template
from mako.lookup import TemplateLookup



class BaseController:

    def __init__(self,userid,templateName='',templateDir='./'):
	self.templateLookup = TemplateLookup(directories=[templateDir,"template"])
	self.setTemplateName(templateName)
	self.setUserID(userid)

    def setTemplateName(self,theName):
	self.templateName = theName


    def setUserID(self,userid):
	self.userID = userid


    def renderPage(self,**options) :
	# Read in the necessary mako template classes
	t = self.templateLookup.get_template(self.templateName)

	# Print out the http header. (Assumes everything that follows is
	# printable material if it is commented out!)
	print("Content-Type: text/html\n\n")
	print(t.render(templateDir="template",**options))


    def sideBar(self,loggedIn=False):
	if(loggedIn):
	    return("<%include file=\"loginBox.tmpl\"/>")
	else:
	    return("")
	    
    def mainContent(self,**options):
	t  = self.templateLookup.get_template('frontPageIntroduction.tmpl')
	return(t.render(templateDir="template".options))


class ClassController(BaseController):

    def __init__(self,userid,templateName='',templateDir='./'):
	BaseController.__init__(self,userid,templateName,templateDir)

    def mainContent(self,**options):
	t  = self.templateLookup.get_template('classPageOverview.tmpl')
	return(t.render(templateDir="template".options))


class LabController(BaseController):

    def __init__(self,userid,templateName='',templateDir='./'):
	BaseController.__init__(self,userid,templateName,templateDir)

    def mainContent(self,**options):
	t  = self.templateLookup.get_template('labPageOverview.tmpl')
	return(t.render(templateDir="template".options))


class LabResultsController(BaseController):

    def __init__(self,userid,templateName='',templateDir='./'):
	BaseController.__init__(self,userid,templateName,templateDir)

    def mainContent(self,**options):
	t  = self.templateLookup.get_template('laboratoryData.tmpl')
	return(t.render(templateDir="template".options))




if (__name__ =='__main__') :
    import sys
    import os
    sys.path.append( os.path.join( os.getcwd(), '..' ) )

    #local classes for Numb3r L0ck3r
    from config.Config import Config
    localConfig = Config('../')
    localConfig.parseConfigurationFile()

    # get the controler to print the page
    from Controller.BaseController import LabResultsController
    #print(localConfig.diskOptions['templateDir'])
    mainControl = LabResultsController('basePage.tmpl',localConfig.diskOptions['templateDir'])
    mainControl.renderPage(loginBox = '',
			   username='',
			   **localConfig.getConfigurationDict())

