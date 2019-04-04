###########################################################
## File        : ViewSet.py
## Description : 
# Class Dependencies

import rest_framework.viewsets

class ViewSet(rest_framework.viewsets.ViewSet):

# Class Attributes

    renderer_classes=(rest_framework.renderers.JSONRenderer, )

# Constructor

    def __init__(self,**kwargs):

# Instance Attributes


# Class Initialisation
        return

# Operations

    @property
    def query(self):
        return
    def get_data(self,criteria):
        return
    def retrieve(self,request,pk=None):
        return
    def list(self,request):
        return
    def set_data(self,data,user):
        return
    def create(self,request):
        return
    def update(self,request,pk=None):
        return
    def remove_data(self,data,user):
        return
    def destroy(self,request,pk=None):
        return
    def partial_update(self,request,pk=None):
        return

