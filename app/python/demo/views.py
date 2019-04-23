###########################################################
## File        : Views.py
## Description : 
"""
This module implements the views and REST api. Entries in the ``urls.py`` list 
map to functions in this module.

Two 'convenience' decorators are used to wrap the underlying functions:

``@RequestToResponse`` - Automatically provides a JSON response to a request
``@WithCursor`` - Provides a connected database cursor to use within a function

"""

import os
import time
import re
import json
import jsonpath

import logging
logging.basicConfig(level=logging.DEBUG)

from django.conf import settings
from django.shortcuts import render_to_response, render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie

from django.db import connection
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test, login_required

from . import definitions

def conditionally(decorator, condition):
    def decorated_result(f):
        if not condition:
            return f
        return decorator(f)
    return decorated_result

def RequestToResponse(function):
    try:
        def decorated_function(*args, **kwargs):
            result = function(*args, **kwargs)
            response = render_to_response('json.html', {"jsonString": mark_safe(result[1])}) # The string needs to be part of a dictionary for the subtitution to work
            if result[0]:
                response.status_code = 200
            else:
                response.status_code = 500
            response['Content-Type'] = 'application/json'
            response['Access-Control-Allow-Origin'] = '*'
            return response
        return decorated_function
    except Exception as e:
        logging.error('Exception: %s'%str(e))
        return ('Exception: %s'%str(e))
    return

def WithCursor(function):
    try:
        def decorated_function(*args, **kwargs):
            with connection.get_new_connection(connection.get_connection_params()) as localConnection:
                with localConnection.cursor() as localCursor:
                    return function(localCursor, *args, **kwargs)
        return decorated_function
    except Exception as e:
        logging.error('Exception: %s'%str(e))
        return ('Exception: %s'%str(e))
    return

def convert_results(results_string):
    # Turns out we need to handle \r, \n, \t and \" ourselves. Thanks Postgres!
    results_string = re.sub(r'\r', r'\\r', results_string);
    results_string = re.sub(r'\n', r'\\n', results_string);
    results_string = re.sub(r'\t', r'\\t', results_string);
    return results_string

#@ensure_csrf_cookie # Uncommenting will break unit test
def home(request, *args, **kwargs):
    """
    The home page ensures that a CSRF cookie is returned to the client.
    """
    logging.info('views.home')
    try:
        #user = request.user.username
        user = 'simon'
        logging.info('  user: %s'%user)
        #email = request.user.email
        email = 'simon.bell@epfl.ch'
        logging.info('  email: %s'%email)
        #name = request.user.name
        name = 'Simon BELL'
        logging.info('  name: %s'%name)
        return render_to_response('index.html', {'user': user, 'email': email, 'name': name}) # 'institution': institution, 
    except Exception as e:
        logging.error('Exception: %s'%str(e))
        return HttpResponse('Exception: %s'%str(e), None, None)

@RequestToResponse
def get_entities(request):
    """
    Retrieve a list of entity definitions.
    """
    logging.info('views.get_entities')
    return get_data_json('demo__definition', 'label,numeric', 'category=\'EntityType\'', None)

@RequestToResponse
def get_options(request, category, item):
    """
    Retrieve a list of valid options for a specific category and item.
    """
    logging.info('views.get_options')
    return get_options_json(category, item)

@WithCursor
def get_data_json(cursor, table, columns, criteria, path):
    """
    """
    logging.info('views.get_data_json')
    try:
        sqlStatement = "select app_get_data_json('%s', '%s', '%s')"%(table, columns, criteria.replace("'","''''"))
        logging.info(sqlStatement)
        cursor.execute(sqlStatement)
        jsonList = cursor.fetchone()[0] # ...as a list of dicts
        if not path == None: # Use this to return an array of primitives, rather than objects
            jsonList = [v[path] for i,v in enumerate(jsonList)]
        jsonString = json.dumps(jsonList)
        return (True, jsonString,)
    except Exception as e:
        logging.error('Exception: %s'%str(e))
        return (False, '{"Error": "%s"}'%str(e),)

@WithCursor
def get_options_json(cursor, category, item):
    logging.info('views.get_options_json')
    try:
        sqlStatement = "select demo_get_options('%s','%s')"%(category, item) # Get Postgres to serve up JSON objects...
        logging.info(sqlStatement)
        cursor.execute(sqlStatement)
        jsonList = cursor.fetchone()[0] # ...as a list of dicts
        if jsonList == None:
            jsonString = '[]'
        else:
            jsonFilteredList = ['{%s}'%','.join(['"label": "%s"'%v['label'], '"numeric": %s'%str(v['numeric']), '"alphanumeric": "%s"'%v['alphanumeric']]) for i,v in enumerate(jsonList)] # List comprehension
            jsonFilteredList = ','.join(jsonFilteredList) # Convert to a string
            jsonString = '[%s]'%convert_results(jsonFilteredList) # Wrap in an array
        return (True, jsonString,)
    except Exception as e:
        logging.error('Exception: %s'%str(e))
        return (False, '{"Error": "%s"}'%str(e),)

from django.utils.decorators import method_decorator

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

