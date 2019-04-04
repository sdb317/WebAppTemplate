###########################################################
## File        : PersonViewSet.py
## Description : 
# Class Dependencies

from . import viewSet

class PersonViewSet(viewSet.ViewSet):

# Class Attributes

    serializer_class=personSerializer.PersonSerializer

# Constructor

    def __init__(self,**kwargs):

# Instance Attributes


# Class Initialisation
        return

# Operations

    @property
    def query(self):
        return
    def retrieve(self,request,pk=None):
        return
    def list(self,request):
        return
    def create(self,request):
        return
    def update(self,request,pk=None):
        return
    def destroy(self,request,pk=None):
        return

