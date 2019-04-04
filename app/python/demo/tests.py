###########################################################
## File        : test.py
## Description : 

import sys
import os
import re
import time
import fnmatch
import csv
import fileinput

import urlparse
import json

from django.conf import settings
from django.test import TestCase, Client
from django.test.runner import DiscoverRunner
from django.db.models.loading import get_models
from rest_framework.test import APIClient
from rest_framework import status

import mock
from . import websitePublicationViewSet

class DiscoverRunnerForPLUS(DiscoverRunner):
    """
    An override of Django's test runner that avoids creation of a test database (see TEST_RUNNER in local.py)
    """

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests)
        result = self.run_suite(suite)
        self.teardown_test_environment()
        return self.suite_result(suite, result)

###########################################################
## Django REST Framework
## 

from demo.models import Person

 class PersonTestCases(TestCase):
     fixtures = ['persons.json']
     url = fullURL('persons')

     def test_person_get(self):
         client = APIClient()
         # get all persons
         response = client.get(self.url, format='json')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertGreaterEqual(len(response.data), 1)
         # get one person
         response = client.get(self.url + '1/', format='json')
         content = json.loads(response.content)
         # compare to value in fixture
         self.assertEqual(content['name'], 'Result Presentation')

     def test_person_post(self):
         client = APIClient()
         # check if new person can be created
         response = client.post(self.url, {
             'name': 'test'
         }, format='json')
         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

     def test_person_delete(self):
         client = APIClient()
         person = Person(name='test')
         person.save()
         # check if newly created person is api accessible
         response = client.get('{}{}/'.format(self.url, person.id), format='json')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         # delete via api
         response = client.delete('{}{}/'.format(self.url, person.id), format='json')
         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
         # check again if api accessible
         response = client.get('{}{}/'.format(self.url, person.id), format='json')
         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

     def test_person_update(self):
         client = APIClient()
         person = Person(name='test')
         person.save()
         # update newly created object via api
         response = client.put('{}{}/'.format(self.url, person.id), {
             'name': 'updated'
         }, format='json')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         response = client.get('{}{}/'.format(self.url, person.id), format='json')
         # get object again via api and check if value was updated
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         content = json.loads(response.content)
         self.assertEqual(content['name'], 'updated')

if __name__=='__main__': # Only used if run outside of Django
    try:
        print("Starting tests")
        # unittest.main() # Run all tests
        suite=unittest.TestSuite() # ...or select tests to run using 'TestSuite'
        #suite.addTest(MyTestCases('<MethodName>')) # Add the test method name here
        unittest.TextTestRunner(verbosity=1).run(suite)
        print("Finished tests")
    except Exception as e:
        print('Exception: %s'%str(e))

