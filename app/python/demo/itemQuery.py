###########################################################
## File        : ItemQuery.py
## Description : 

import logging
logging.basicConfig(level=logging.DEBUG)

import re
import json

# Class Dependencies

from . import optimisedModels

class ItemQuery(optimisedModels.OptimisedModels):

# Class Attributes


# Constructor

    def __init__(self,table):

# Instance Attributes


# Class Initialisation
        super(ItemQuery, self).__init__(table)
        return

# Operations

    def Execute(self,criteria,sqlCriteria,parse):
        """
        Retrieve a list of items that match the criteria specified
        """
        logging.info('ItemQuery.Execute')
        try:
            jsonCriteria = json.loads(criteria) # Convert string to object
            if jsonCriteria[u'Criteria'][u'FundingPeriod'] != None:
                if len(sqlCriteria):
                    sqlCriteria += " and "
                sqlCriteria += "(task.phase=''%s'')"%(jsonCriteria[u'Criteria'][u'FundingPeriod'])
            if jsonCriteria[u'Criteria'][u'SubProject'] != None:
                if len(sqlCriteria):
                    sqlCriteria += " and "
                sqlCriteria += "(subproject.hbp_id=''%s'')"%('SP'+re.search(r'(?:\D{1,2})?(\d{1,2})',jsonCriteria[u'Criteria'][u'SubProject']).group(1))
            if jsonCriteria[u'Criteria'][u'WorkPackage'] != None:
                if len(sqlCriteria):
                    sqlCriteria += " and "
                sqlCriteria += "(workpackage.hbp_id like ''%s%%'')"%('WP'+re.sub('^WP','',jsonCriteria[u'Criteria'][u'WorkPackage'],1))
            if jsonCriteria[u'Criteria'][u'Task'] != None:
                if len(sqlCriteria):
                    sqlCriteria += " and "
                sqlCriteria += "(task.hbp_id like ''%s%%'')"%('T'+re.sub('^T','',jsonCriteria[u'Criteria'][u'Task'],1))
            sqlStatement = self.getSqlStatement()
            if len(sqlCriteria):
                results = super(ItemQuery, self).Execute(sqlStatement%(sqlCriteria), parse)
            else:
                results = []
            return (True, results,)
        except Exception as e:
            logging.error('Exception: %s'%str(e))
            return (False, None,)

