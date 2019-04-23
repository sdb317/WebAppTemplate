###########################################################
## File        : OptimisedModels.py
## Description : 
"""
Django database interations are optimised for CRUD operations. When queries become 
complex, this model is very inefficient.
This module implements provides base functionality for optimising queries and commands.

The following decorators are used to wrap the underlying functions:

``@WithCursor`` - Provides a connected database cursor to use within a function

"""

import logging
logging.basicConfig(level=logging.DEBUG)

import re
import json

from . import definitions

from . import managedConnection

def WithCursor(function):
    try:
        def decorated_function(*args, **kwargs):
            with managedConnection.ManagedConnection() as localConnection:
                with localConnection.cursor() as localCursor:
                    return function(localCursor, *args, **kwargs)
        return decorated_function
    except Exception as e:
        logging.error('Exception: %s'%str(e))
        return ('Exception: %s'%str(e))
    return

# Class Dependencies

from . import models

class OptimisedModels(models.PermissionModel):

# Class Attributes


# Constructor

    def __init__(self,table):

# Instance Attributes

        self.table=table

# Class Initialisation

        return

# Operations

    def get(self,criteria):
        sqlCriteria = ''
        detail = False
        if 'detail' in criteria['Criteria'] and criteria['Criteria']['detail'] == 'true':
            detail = True
        audit = False
        if 'audit' in criteria['Criteria'] and criteria['Criteria']['audit'] == 'true':
            audit = True
        if 'id' in criteria['Criteria'] and criteria['Criteria']['id'] != None:
            sqlCriteria += "(%s.id=%s)"%(self.table, criteria['Criteria']['id']) # An integer
            detail = True
        if 'saved_by' in criteria['Criteria'] and criteria['Criteria']['saved_by'] != None and len(criteria['Criteria']['saved_by']) > 0: # This is a list of words to search for in publication name field
            if len(sqlCriteria):
                sqlCriteria += " and "
            sqlCriteria += "(%s.saved_by=''%s'' or %s_audit.saved_by=''%s'')"%(self.table, criteria['Criteria']['saved_by'], self.table, criteria['Criteria']['saved_by'])
        return (sqlCriteria,detail,audit)

    def GetTypeForHBPID(self,id):
        if re.match(r'SP\d+', id) != None:
            return definitions.EntityTypeSubProject
        elif re.match(r'WP\d+\.\d+', id) != None:
            return definitions.EntityTypeWorkPackage
        elif re.match(r'T\d+\.\d+\.\d+', id) != None:
            return definitions.EntityTypeTask
        return definitions.EntityTypeUnknown

    def ParseValue(self,value):
        if value is None:
            return "null"
        else:
            if isinstance(value, str):
                return "'%s'"%value.replace("'",r"''")
            else:
                return str(value)

    def Normalise(self,value):
        try:
            newValue = value
            newValue = re.sub(r"\r?\n(?!(([^']*'){2})*[^']*$)",'\\n',newValue) # Replace newlines in quoted strings with \n i.e. don't match if there are even number of quotes ahead of the match
            newValue = re.sub(r"\r?\n(?=(([^']*'){2})*[^']*$)",' ',newValue) # Then Replace newlines outside of quoted strings with a space i.e. do match if there are even number of quotes ahead of the match
            newValue = re.sub(r'[ \t]+',' ',newValue) # Then remove unnecessary spaces and tabs
            return newValue
            #return value
        except Exception as e:
            logging.error('Exception: %s'%str(e))
            logging.error('value: %s'%value)
            return value # If there is a problem with the regexp
        return

    @WithCursor
    def Execute(cursor,self,statement,parse):
        statement = self.Normalise(statement)
        logging.debug(statement)
        cursor.execute(statement)
        results = cursor.fetchone()[0] # A list of dicts
        if results == None:
            return '[]' # An empty list
        else:
            if parse != None:
                results = parse(results) # Apply any filter lambda
            else:
                if type(results) is int:
                    return results
        return json.dumps(results) # Convert to a string, derived classes need to catch exceptions and handle appropriately

