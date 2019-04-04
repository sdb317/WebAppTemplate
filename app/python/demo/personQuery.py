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
            jsonCriteria = json.loads(criteria) # Convert string to object
            if 'first_name' in jsonCriteria['Criteria'] and jsonCriteria['Criteria']['first_name'] != None:
                if len(sqlCriteria):
                    sqlCriteria += " and "
                sqlCriteria += "(person.first_name=''%s'')"%(jsonCriteria['Criteria']['first_name'])
                detail = True
            if 'last_name' in jsonCriteria['Criteria'] and jsonCriteria['Criteria']['last_name'] != None:
                if len(sqlCriteria):
                    sqlCriteria += " and "
                sqlCriteria += "(person.last_name=''%s'')"%(jsonCriteria['Criteria']['last_name'])
                detail = True
            if 'email' in jsonCriteria['Criteria'] and jsonCriteria['Criteria']['email'] != None:
                if len(sqlCriteria):
                    sqlCriteria += " and "
                sqlCriteria += "(lower(person.email) like lower(''%%%s%%''))"%(jsonCriteria['Criteria']['email'].replace("'","''''")) # Contains
            if 'type' in jsonCriteria['Criteria'] and jsonCriteria['Criteria']['type'] != None and int(jsonCriteria['Criteria']['type']) != definitions.OptionPersonTypeUnknown:
                if len(sqlCriteria):
                    sqlCriteria += " and "
                sqlCriteria += "(person.type=%s)"%(jsonCriteria['Criteria']['type']) # Integer
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
            publication = instance
            publication_id = publication['id']
            links = ','.join(['row(%d,%d,%d)'%(publication['id'],i['value'],i['type'],) for i in publication['links']])
            links = 'array[%s]::plus_link_type[]'%links
            sqlStatement = ""
            sqlStatement += self.ParseValue(person['email'])
            sqlStatement += ", "
            sqlStatement += self.ParseValue(person['first_name'])
            sqlStatement += ", "
            sqlStatement += self.ParseValue(person['last_name'])
            sqlStatement = u"select demo_save_person(%s, %d, %s, %s)"%(
                self.ParseValue(user),
                self.ParseValue(person_id),
                links,
                sqlStatement
                )
            logging.info(sqlStatement)
            publication_id = self.Execute(sqlStatement, None)
            return (True, '{"Success": %s}'%publication_id,)
        except Exception as e:
            logging.error('Exception: %s'%str(e))
            return (False, '{"Error": "%s"}'%str(e),)
        return

    def remove(self,instance,user):
        try:
            publication = instance
            publication_id = publication['id']
            sqlStatement = u"select demo_remove_person(%s, %d)"%(
                self.ParseValue(user),
                self.ParseValue(person_id),
                )
            logging.info(sqlStatement)
            publication_id = self.Execute(sqlStatement, None)
            return (True, '{"Success": %s}'%publication_id,)
        except Exception as e:
            logging.error('Exception: %s'%str(e))
            return (False, '{"Error": "%s"}'%str(e),)
        return

