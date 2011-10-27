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

import logging
import pickle
import os
import os.path

from ..common import version 

version.getInstance().submitRevision("$Revision: 155 $")

def get_maegen_storage_dir():
    '''
    Compute the application storage dir.
    This is an utility function to retrieve the directory where zourite can
    store any file like settings or cached data.
    '''
    storage = os.path.expanduser("~")
    storage = os.path.join(storage, "MyDocs")
    storage = os.path.join(storage, ".documents")
    return storage

class Maegen(object):
    '''
    Main class of the Program. The GUI use this class like a Facade to any core functions.
    '''
    
    def __init__(self):
        self._ensure_maegen_conf_store()
        self.database = Database()
        
        
        
    
    def _ensure_maegen_conf_store(self):
        storage = get_maegen_storage_dir()
        if os.path.exists(storage):
            pass
        else:
            os.makedirs(storage)

    
    def _save_database(self, filename):
        '''
        Save the current database into a file
        '''
        pass
    
    def _load_database(self, filename):
        '''
        Read a database from a file. The new database become the current database. 
        '''
        pass
    
    '''
    Facade function
    '''
    
    def get_families_for(self, individual):
        '''
        Return all family where thi given individual is a parent.
        '''
        def parent_in(individual):
            return lambda x: individual  in [x.husband, x.wife] 
            
        return filter(parent_in(individual), self.database.families)
    
    def individuals_count(self):
        '''
        Return the number of individual in the current database
        '''
        return len(self.database.individuals)
    
    def families_count(self):
        '''
        Return the number of families in the current database
        '''
        return len(self.database.families)
    
    def branches_count(self):
        '''
        Return the count of branches (tree) in the database
        '''
        logging.warning("not yet implemented")
        return 0
    
    def names_count(self):
        '''
        return the count of patronymic name in the database
        '''
        logging.warning("not yet implemented")
        return 0

    def create_new_individual(self, name="inconnu", firstname="inconnu"):
        '''
        Create a new individual and add it to the database
        Return a new individual
        '''
        resu = Individual()
        resu.name = name
        resu.firstname = firstname
        self.database.individuals.add(resu)
        return resu
    
    def create_new_family(self, husband, wife):
        '''
        Create a new family
        '''
        resu = Family()
        resu.husband = husband
        resu.wife = wife
        self.database.families.add(resu)
        return resu
    
    def make_child(self,individual, family):
        '''
        Promote the given individual to child of given family 
        '''
        family.children.append(individual)
        individual.father = family.husband
        individual.mother = family.wife
    
    def retrieve_all_individuals(self):
        '''
        return all individuals in the database as a list
        '''
        return list(self.database.individuals)
    
    def retrieve_all_families(self):
        '''
        return all families in the database as a list
        '''
        return list(self.database.families)
        

    def get_maegen_storage_dir(self):
        '''
        Storage location of megen database
        '''
        return get_maegen_storage_dir()

    
    def load_database(self, database_file):
        '''
        Read a database from a file
        '''        
        self._load_database(filename)


    def save_database(self, database_file):
        '''
        Write current database into a file
        '''
        self._save_database(database_file)
        
    def create_new_database(self, database_file):
        '''
        Create a new empty database
        '''
        self.database = Database()
        self._save_database(database_file)
        
'''
Model of genealogical data
'''

class Database(object):
    """
    genealogical data consist in a set of individuals related by a set of families
    """
    def __init__(self):
        self.individuals = set([])
        self.families = set([])

class Individual(object):
    '''
    A person
    '''
    def __init__(self):
        self.name = ""
        self.firstname = ""
        self.nickname = ""        
        self.gender = None
        
        self.birthDate = None
        self.birthPlace = ""        
        self.deathDate = None
        self.deathPlace = ""
        
        self.note = ""
        
        self.father = None
        self.mother = None
        
        self.occupation = ""

    def __str__(self, *args, **kwrgs):
        return self.firstname.capitalize() + " " + self.name.upper()

    
    
    
class Family(object):
    '''
    A family
    '''
    
    def __init__(self):
        self.husband = None
        self.wife = None
        self.married = False
        self.divorced = False
        self.divorced_date= None
        self.married_date = None
        self.married_place = ""
        
        self.children = []
                

            