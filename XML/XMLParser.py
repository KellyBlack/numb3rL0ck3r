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

# This is the class used as a base class for parsing xml files.
# It is called by any class that has to take an xml file and
# traverse its tree.

import xml.sax     #.handler

class XMLParser (xml.sax.handler.ContentHandler):

    DEBUG = True

    def __init__(self) :
	self.cleanUpXML()


    def __del__(self) :
	self.cleanUpXML()

    def getBuffer(self) :
        return self.XMLStack      #  returns the pointer to the buffer


    def setBuffer(self,value) :
        self.XMLStack = value
        
    def getXMLDocument(self) :
        return self.doc           #  returns the pointer to the document.


    def startDocument(self):
        self.XMLStack = []
        self.currentStack = []
        xml.sax.handler.ContentHandler.startDocument(self)

        if(self.DEBUG):
             print("starting to read the document");


    def endDocument(self):
         if(len(self.currentStack)>0) :
             if(self.DEBUG) :
                 print("There is an error in the XML.")
         self.currentStack = []
         xml.sax.handler.ContentHandler.endDocument(self)

         if(self.DEBUG):
             print("End of the document:\n{0}".format(self.XMLStack));


    def startElement(self, name, attributes):

        self.currentStack.append([name,attributes.copy(),"",[]])
                        
        if(self.DEBUG) :
            for child in attributes.getNames():
                print("Child: {0} - {1}".format(child,attributes.getValue(child)))

        self.currentName = name
        if(name == "objectclass"):
              pass

    def characters(self,data) :
        last = self.currentStack[-1]
        last[-2] += data

    def endElement(self, name):

        thisElement = []
        if((type(self.currentStack) is list) and (len(self.currentStack)>0)) :
             thisElement = self.currentStack.pop()
        else:
             if(self.DEBUG):
                 print("There is an error in the xml file.")

        if((type(self.currentStack) is list) and (len(self.currentStack)>0)) :
            previousElement = self.currentStack.pop()
            previousElement[-1].append(thisElement)
            self.currentStack.append(previousElement)

        else :
            # This is a top level element.
            self.XMLStack.append(thisElement)
            previousElement = [""]

        #if(self.DEBUG) :
        #       print("End: {0}".format(name))
        #        print("XML Stack: {0}".format(self.XMLStack))
        #        print("Current Stack: {0}\n\n\n".format(self.currentStack))

                
        self.currentName = previousElement[0]


    ## parseXMLString
    #
    # Parse the contents of an xml string and put them into an
    # XML tree.
    #  
    def parseXMLString(self,xmlString) :
        parser = xml.sax.make_parser([])
        parser.setContentHandler(self)
        parser.reset()
        parser.feed(xmlString)
        parser.close()




    def readXMLFile(self,fileName) :
        # Read an XML file and put it into the local buffer.
        # This routine is mostly in place for testing and
        # debugging 4 the xml codes. 
        #

        parser = xml.sax.make_parser(['IncrementalParser'])
        parser.setContentHandler(self)
        parser.reset()

        file = open(fileName,"r")
        #theXML = ""
        for line in file:
                #theXML += line
                parser.feed(line)
                if(self.DEBUG) :
                    print(line[0:-1])

        parser.close()
        #print(theXML)
        #xml.sax.parseString(theXML,handler)


    def cleanUpDocument(self) :
        # free the document # 
        self.doc = None



    def cleanUpXML(self):
        # Clean up and free the data and variables associated with the parsed
        # XML tree.
        #  

        #  Clean up the document
        self.cleanUpDocument();

        self.XMLStack = []
        self.currentStack = []

        #  initialize the xml parameters
        self.root_node = None;
        self.currentName = ""









if (__name__ =='__main__') :

    handler = XMLParser()
    handler.readXMLFile("networkSample.xml")


    parser = xml.sax.make_parser(['IncrementalParser'])
    handler = XMLParser()
    parser.setContentHandler(handler)
    parser.reset()

    file = open("networkSample.xml","r")
    theXML = ""
    for line in file:
        theXML += line
        parser.feed(line)
        #print(line[0:-1])

    parser.close()
    print(theXML)
    #xml.sax.parseString(theXML,handler)


    
