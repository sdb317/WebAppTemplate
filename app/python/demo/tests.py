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

import json

from django.conf import settings
from django.test import TestCase, Client
from django.test.runner import DiscoverRunner
from rest_framework.test import APIClient
from rest_framework import status

import mock

# python app\python\manage.py test demo.debug.MyTestCases.test<TestName>

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

class MyTestCases(TestCase):

    @classmethod
    def setUpClass(cls):
        '''Call on class creation.'''
        print('Calling \'setUpClass\'')
        super(MyTestCases, cls).setUpClass()

    def setUp(self):
        '''Call before every test case.'''
        print('Calling \'setUp\'')

    def tearDown(self):
        '''Call after every test case.'''
        print('Calling \'tearDown\'')

    '''Test cases. Note that all test method names must begin with 'test'.'''

    def testPersonModel(self):
        try:
            import models
            persons = models.Person.objects.filter(first_name='Simon')
            assert True
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testHomePage(self):
        print('Calling \'testHomePage\'')
        try:
            #mock_render_to_response = mock.MagicMock()
            with mock.patch.multiple( \
                'demo.views', \
                #render_to_response=mock_render_to_response, \ # Use a real 'render_to_response' and test the returned HttpResponse object instead
                RequestContext=mock.MagicMock(), \
                login_required=lambda x: x, \
                user_passes_test=lambda x: x \
                ):
                from views import home
                mock_request = mock.Mock()
                mock_request.user.username = 'simon'
                result = home(mock_request)
                #_, args, _ = mock_render_to_response.mock_calls[0] # Could examine the template data here
            assert result.status_code == 200 and result.content.find(r'<h1>Welcome Simon</h1>') != -1
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testPersonQueryGet(self): # test demo.tests.MyTestCases.testPersonQueryGet
        print('Calling \'testPersonQueryGet\'')
        try:
            import personQuery
            test = personQuery.PersonQuery('person')
            results = test.get('{"Criteria": {"first_name": null, "last_name": null, "email": null, "type": null}}')
            self.assertTrue((re.search(r'Persons', str(results)) != None), r'Unexpected contents')
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testPersonQuerySet(self): # test demo.tests.MyTestCases.testPersonQuerySet
        print('Calling \'testPersonQuerySet\'')
        try:
            import personQuery
            test = personQuery.PersonQuery('person')
            payload = \
                """
                {
                    "first_name": "Simon",
                    "last_name": "Bell",
                    "email": "",
                    "type": 1,
                    "links":[
                    ]
                }
                """
            result = test.set(json.loads(payload), 'simon')
            self.assertTrue((re.search(r'Success', str(result)) != None), r'Unexpected contents')
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testPersonViewSetCreate(self): # test demo.tests.MyTestCases.testPersonViewSet
        print('Calling \'testPersonViewSetCreate\'')
        try:
            import personViewSet
            #mock_render_to_response = mock.MagicMock()
            with mock.patch('plus.personViewSet'):
                mock_request = mock.Mock()
                mock_request.body = \
                    """
                    {
                        "id":1,
                        "first_name": "Simon",
                        "last_name": "Bell",
                        "email": "",
                        "type": 1,
                        "links":[
                        ]
                    }
                    """
                test = personViewSet.PersonViewSet()
                result = test.create(mock_request)
                #_, args, _ = mock_render_to_response.mock_calls[0] # Could examine the template data here
            assert result.status_code == 200 and result.data['Success'] > 1
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testGetDataJSON(self): # test demo.tests.MyTestCases.testGetDataJSON
        print('Calling \'testGetDataJSON\'')
        try:
            from .views import get_data_json
            result = get_data_json('demo__definition', 'label,numeric', 'category=\'EntityType\'', None)
            if result[0]:
                print(result[1])
                assert len(result[1]) > 0
                return
            assert False
        except Exception as e:
            assert False,'Exception: %s'%str(e)

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

