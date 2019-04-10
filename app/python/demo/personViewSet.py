###########################################################
## File        : PersonViewSet.py
## Description : 

import logging
logging.basicConfig(level=logging.DEBUG)

from . import personSerializer
from . import personQuery

# Class Dependencies

from . import viewSet

class PersonViewSet(viewSet.ViewSet):

# Class Attributes

    serializer_class=personSerializer.PersonSerializer

# Constructor

    def __init__(self,**kwargs):

# Instance Attributes


# Class Initialisation
        super().__init__(**kwargs)
        return

# Operations

    @property
    def query(self):
        return personQuery.PersonQuery(u'person')

    def retrieve(self,request,pk=None):
        logging.info('PersonViewSet.retrieve')
        return super(PersonViewSet, self).retrieve(request,pk)

    def list(self,request):
        logging.info('PersonViewSet.list')
        return super(PersonViewSet, self).list(request)

    def create(self,request):
        logging.info('PersonViewSet.create')
        return super(PersonViewSet, self).create(request)

    def update(self,request,pk=None):
        logging.info('PersonViewSet.update')
        return super(PersonViewSet, self).update(request,pk)

    def destroy(self,request,pk=None):
        logging.info('PersonViewSet.destroy')
        return super(PersonViewSet, self).destroy(request,pk)

