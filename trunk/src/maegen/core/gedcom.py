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
Created on Nov 2, 2011

@author: maemo
'''

from string import Template

#from ..common import version 

#version.getInstance().submitRevision("$Revision: 155 $")

class GedcomWriter():
    '''
    This class can export a maegen database into GEDCOM format 
    '''
    def __init__(self, database):
        '''
        Create a writer that can export a maegen database into GEDCOM format
        Parameter:
            - database : the maegen database
        '''
        self.database = database
    
    
    
    def export(self):
        '''
        Return a GEDCOM string for the current database
        '''
        return self._create_header() + self._create_submitter() + self._create_record() + self._create_trlr()
        
    def _create_header(self):
        '''
        Return the header for the current database
        '''
        header = \
"""0 HEAD
1 SOUR Maegen
2 VERS $version_of_maegen
1 SUBM @SUBMITTER@ 
1 GEDC
2 VERS 5.5
2 FORM LINEAGE-LINKED      
"""        
        return Template(header).substitute(version_of_maegen="1.0")
    
    def _create_submitter(self):
        submitter = \
"""0 @SUBMITTER@ SUBM
1 NAME $submitter
""" 
        # TODO replace maemo by the user name
        return Template(submitter).substitute(submitter="maemo")
        
    def _create_record(self):
        # TODO 
        return ""
    
    def _create_trlr(self):
        return "0 TRLR"
    
    
if __name__ == '__main__':  
    print GedcomWriter(None).export()