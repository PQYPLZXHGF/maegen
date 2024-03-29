# -*- encoding: UTF-8 -*-

#    Maegen is a genealogical application for N900. Use it on the go
#    to store genealogical data including individuals and relational
#    informations. Maegen can be used to browse collected data on the
#    device but the main goal is its capabilitie to export the dtabase
#    in a GEDCOM file which can be imported into any desktop genealocial
#    application.
#
#    Copyright (C) 2011  Thierry Bressure
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
'''
Created on Oct 14, 2011

@author: maemo
'''

CURRENT_VERSION = "0.3.0-SNAPSHOT"  # this must be modified before any release

def getInstance():
    return SINGLETON

class Version(object):
    '''
    Hold the revision of the application.
    '''        

    def __init__(self):
        '''
        Constructor
        '''
        self.revision = ""
        
    def submitRevision(self, rev):
        '''
        submit a new revision. If the revision is upper than
        the current revision, it become the new current revision
        '''
        
        if self.revision < rev:
            self.revision = rev
            
    def getRevision(self):
        '''
        Return the scm revision for this application
        '''
        return self.revision
    
    def getVersion(self):
        '''
        Return the marketing version for this application.
        '''
        return CURRENT_VERSION
    
SINGLETON = Version()  # object that track the revision of current applcation for issue tracking purpose

getInstance().submitRevision("$Revision$")
