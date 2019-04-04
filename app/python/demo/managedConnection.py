###########################################################
## File        : ManagedConnection.py
## Description : 
"""
Used by the @WithCursor decorator to ensure connections are released after use

"""

from django.db import connection

# Class Dependencies

class ManagedConnection():

# Class Attributes

# Operations

    def __init__(self):
        return

    def __enter__(self):
        self.connection = connection.get_new_connection(connection.get_connection_params())
        self.connection.autocommit = True
        return self.connection

    def __exit__(self,type,value,trace):
        self.connection.close()
        return

