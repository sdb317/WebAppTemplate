###########################################################
## File        : PersonSerializer.py
## Description : 
# Class Dependencies

from . import baseSerializer

class PersonSerializer(baseSerializer.BaseSerializer):

# Class Attributes


# Constructor

    def __init__(self,**kwargs):

# Instance Attributes


# Class Initialisation
        super().__init__(**kwargs)
        return

# Operations

    @property
    def data(self):
        return super().data

    def create(self,validated_data):
        return

    def update(self,instance,validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return

