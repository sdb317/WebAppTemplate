###########################################################
## File        : ViewSet.py
## Description : 

import logging
logging.basicConfig(level=logging.DEBUG)

import json

from django.http import JsonResponse

import rest_framework.authentication
import rest_framework.permissions
import rest_framework.renderers
from rest_framework.permissions import IsAuthenticated

# Class Dependencies

import rest_framework.viewsets

class ViewSet(rest_framework.viewsets.ViewSet):

# Class Attributes

    renderer_classes=(rest_framework.renderers.JSONRenderer, )

# Constructor

    def __init__(self,**kwargs):

# Instance Attributes


# Class Initialisation

        #super(ViewSet, self).__init__(**kwargs)
        return

# Operations

    @property
    def query(self):
        raise Exception('Error: ViewSet.query') # Pure virtual - must be implemented in derived class
        return

    def get_data(self,criteria):
        results = self.query.get(criteria)
        if not results[0]:
            raise Exception('Error: ViewSet.get')
        return json.loads(results[1])

    def retrieve(self,request,pk=None):
        try:
            audit = ''
            if request.query_params.get('audit') != None:
                audit = '"audit": "true",'
            criteria = json.loads(r'{"Criteria": {%s "id": %s}}'%(audit,pk,))
            serializer = self.serializer_class(data=self.get_data(criteria))
            return rest_framework.response.Response(serializer.initial_data)
        except Exception as e:
            return JsonResponse(data={'message': 'Error: ViewSet.retrieve - '%e.message}, status=500)
        return

    def list(self,request):
        try:
            criteria = json.loads(r'{"Criteria": %s}'%json.dumps(request.query_params))
            serializer = self.serializer_class(data=self.get_data(criteria))
            return rest_framework.response.Response(serializer.initial_data)
        except Exception as e:
            return JsonResponse(data={'message': 'Error: ViewSet.list - '%e.message}, status=500)
        return

    def set_data(self,data,user):
        results = self.query.set(data, user)
        if not results[0]:
            raise Exception('Error: ViewSet.set')
        return json.loads(results[1])

    def create(self,request):
        try:
            data = request.data
            result = self.set_data(data, request.user.username)
            return rest_framework.response.Response(result)
        except Exception as e:
            return JsonResponse(data={'message': 'Error: ViewSet.create - '%e.message}, status=500)
        return

    def update(self,request,pk=None):
        try:
            data = request.data
            data[u'id'] = int(pk)
            result = self.set_data(data, request.user.username)
            return rest_framework.response.Response(result)
        except Exception as e:
            return JsonResponse(data={'message': 'Error: ViewSet.update - '%e.message}, status=500)
        return

    def remove_data(self,data,user):
        results = self.query.remove(data, user)
        if not results[0]:
            raise Exception('Error: ViewSet.set')
        return json.loads(results[1])

    def destroy(self,request,pk=None):
        try:
            data = {}
            data[u'id'] = int(pk)
            serializer = self.serializer_class(data=data)
            result = self.remove_data(serializer.initial_data, request.user.username)
            return rest_framework.response.Response(result)
        except Exception as e:
            return JsonResponse(data={'message': 'Error: ViewSet.destroy - '%e.message}, status=500)
        return

    def partial_update(self,request,pk=None):
        raise Exception('Error: ViewSet.partial_update') # Not implemented
        return

