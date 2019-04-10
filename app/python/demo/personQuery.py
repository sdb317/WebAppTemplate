###########################################################
## File        : PersonQuery.py
## Description : 

import logging
logging.basicConfig(level=logging.DEBUG)

import re
import json

import definitions

# Class Dependencies

from . import optimisedModels

class PersonQuery(optimisedModels.OptimisedModels):

# Class Attributes


# Constructor

    def __init__(self,table):

# Instance Attributes


# Class Initialisation
        super().__init__(table)
        return

# Operations

    def get(self,criteria):
        """
        Retrieve a list of persons that match the criteria specified in the following JSON format:
            {
               "Criteria": {
                  "first_name": null,
                  "last_name": null,
                  "email": null,
                  "type": null
               }
            } 
        If the criterion exists, add it to the 'where' clause
        """
        logging.info('PersonQuery.Execute')
        try:
            (sqlCriteria,detail,audit) = super().get(criteria) 
            if 'first_name' in criteria['Criteria'] and criteria['Criteria']['first_name'] != None:
                if len(sqlCriteria):
                    sqlCriteria += " and "
                sqlCriteria += "(person.first_name=''%s'')"%(criteria['Criteria']['first_name'])
                detail = True
            if 'last_name' in criteria['Criteria'] and criteria['Criteria']['last_name'] != None:
                if len(sqlCriteria):
                    sqlCriteria += " and "
                sqlCriteria += "(person.last_name=''%s'')"%(criteria['Criteria']['last_name'])
                detail = True
            if 'email' in criteria['Criteria'] and criteria['Criteria']['email'] != None:
                if len(sqlCriteria):
                    sqlCriteria += " and "
                sqlCriteria += "(lower(person.email) like lower(''%%%s%%''))"%(criteria['Criteria']['email'].replace("'","''''")) # Contains
            if 'type' in criteria['Criteria'] and criteria['Criteria']['type'] != None and int(criteria['Criteria']['type']) != definitions.OptionPersonTypeUnknown:
                if len(sqlCriteria):
                    sqlCriteria += " and "
                sqlCriteria += "(person.type=%s)"%(criteria['Criteria']['type']) # Integer
            sqlStatement = \
                """
	            select
		            demo_find_person
			            (
                        '%s',
                        %s,
                        %s
			            );
                """
            results = self.Execute(sqlStatement%((sqlCriteria if len(sqlCriteria) else 'true'),('true' if detail else 'false'),('true' if audit else 'false')), None)
            return (True, '{"Persons": %s}'%results,) # Wrap in a 'Persons' object
        except Exception as e:
            logging.error('Exception: %s'%str(e))
            return (False, '{"Error": "%s"}'%str(e),)
        return

    def set(self,instance,user):
        try:
            person = instance
            person_id = person['id']
            links = ','.join(['row(%d,%d,%d)'%(person['id'],i['value'],i['type'],) for i in person['links']])
            links = 'array[%s]::app_link_type[]'%links
            sqlStatement = ""
            sqlStatement += self.ParseValue(person[u'email'])
            sqlStatement += ", "
            sqlStatement += self.ParseValue(person[u'first_name'])
            sqlStatement += ", "
            sqlStatement += self.ParseValue(person[u'last_name'])
            sqlStatement += ", "
            sqlStatement += self.ParseValue(person[u'type'])
            sqlStatement = u"select demo_save_person(%s, %s, %s, %s)"%(
                self.ParseValue(user),
                self.ParseValue(person_id),
                links,
                sqlStatement
                )
            logging.info(sqlStatement)
            person_id = self.Execute(sqlStatement, None)
            return (True, '{"Success": %s}'%person_id,)
        except Exception as e:
            logging.error('Exception: %s'%str(e))
            return (False, '{"Error": "%s"}'%str(e),)
        return

    def remove(self,instance,user):
        try:
            person = instance
            person_id = person['id']
            sqlStatement = u"select demo_remove_person(%s, %s)"%(
                self.ParseValue(user),
                self.ParseValue(person_id),
                )
            logging.info(sqlStatement)
            person_id = self.Execute(sqlStatement, None)
            return (True, '{"Success": %s}'%person_id,)
        except Exception as e:
            logging.error('Exception: %s'%str(e))
            return (False, '{"Error": "%s"}'%str(e),)
        return

