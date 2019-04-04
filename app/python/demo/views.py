###########################################################
## File        : Views.py
## Description : 
# Class Dependencies

import django.views.generic

class Views(django.views.generic.TemplateView):

# Class Attributes

    template_name='index.html'

# Constructor

    def __init__(self):

# Instance Attributes


# Class Initialisation

        return

# Operations

    @method_decorator(login_required(login_url='/login/hbp'))
    def dispatch(self,*args,**kwargs):
        return

    def get_context_data(self,**kwargs):
        return

