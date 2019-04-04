###########################################################
## File        : BaseSerializer.py
## Description : 
# Class Dependencies

import rest_framework.serializers

class BaseSerializer(rest_framework.serializers.BaseSerializer):

# Class Attributes


# Constructor

    def __init__(self,**kwargs):

# Instance Attributes


# Class Initialisation
        super(BaseSerializer, self).__init__(**kwargs)
        return

# Operations

    def to_internal_value(self,data):
        return

    def to_representation(self,obj):
        return obj

    @property
    def data(self):
        return super(BaseSerializer, self).data

    def create(self,validated_data):
        return

    def update(self,instance,validated_data):
        return

