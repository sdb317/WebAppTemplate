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

# python app\python\manage.py test <app>.debug.MyTestCases

class DiscoverRunnerForApp(DiscoverRunner):
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
        self.app = os.path.basename(os.path.normpath(os.path.dirname(os.path.abspath(__file__))))
        print('App is \'' + self.app + '\'')

    def tearDown(self):
        '''Call after every test case.'''
        print('Calling \'tearDown\'')

    '''Test cases. Note that all test method names must begin with 'test'.'''

    def testPersonModel(self): # test <app>.tests.MyTestCases.testPersonModel
        try:
            from .models import Person
            persons = Person.objects.filter(first_name='Simon')
            assert True
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testGetDataJSON(self): # test <app>.tests.MyTestCases.testGetDataJSON
        print('Calling \'testGetDataJSON\'')
        try:
            from .views import get_data_json
            result = get_data_json(self.app + '__definition', 'label,numeric', 'category=\'EntityType\'', None)
            if result[0]:
                print(result[1])
                assert len(result[1]) > 0
                return
            assert False
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testHomePage(self):
        print('Calling \'testHomePage\'')
        try:
            with mock.patch.multiple( \
                self.app + '.views', \
                RequestContext=mock.MagicMock(), \
                login_required=lambda x: x, \
                user_passes_test=lambda x: x \
                ):
                from .views import home
                mock_request = mock.Mock()
                mock_request.user.username = 'simon'
                mock_request.user.email = 'simon.bell@epfl.ch'
                mock_request.user.name = 'Simon BELL'
                result = home(mock_request)
            assert result.status_code == 200
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testPersonQueryGet(self): # test <app>.tests.MyTestCases.testPersonQueryGet
        print('Calling \'testPersonQueryGet\'')
        try:
            from .personQuery import PersonQuery
            test = PersonQuery('person')
            results = test.get(json.loads('{"Criteria": {"first_name": null, "last_name": null, "email": null, "type": null}}'))
            self.assertTrue((re.search(r'Persons', str(results)) != None), r'Unexpected contents')
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testPersonQuerySet(self): # test <app>.tests.MyTestCases.testPersonQuerySet
        print('Calling \'testPersonQuerySet\'')
        try:
            from .personQuery import PersonQuery
            test = PersonQuery('person')
            payload = \
                """
                {
                    "id":2,
                    "first_name": "Simon",
                    "last_name": "BELL",
                    "email": "simon.bell@epfl.ch",
                    "type": 0,
                    "links":[
                    ]
                }
                """
            result = test.set(json.loads(payload), 'simon')
            self.assertTrue((re.search(r'Success', str(result)) != None), r'Unexpected contents')
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testPersonViewSetList(self): # test <app>.tests.MyTestCases.testPersonViewSetList
        print('Calling \'testPersonViewSetList\'')
        try:
            from .personViewSet import PersonViewSet
            with mock.patch(self.app + '.personViewSet'):
                mock_request = mock.Mock()
                mock_request.query_params = dict()
                test = PersonViewSet()
                result = test.list(mock_request)
            assert result.status_code == 200
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testPersonViewSetCreate(self): # test <app>.tests.MyTestCases.testPersonViewSetCreate
        print('Calling \'testPersonViewSetCreate\'')
        try:
            from .personViewSet import PersonViewSet
            with mock.patch(self.app + '.personViewSet'):
                mock_request = mock.Mock()
                mock_request.user.username = "simon"
                data = \
                    """
                    {
                        "id":2,
                        "first_name": "Simon",
                        "last_name": "BELL",
                        "email": "simon.bell@epfl.ch",
                        "type": 0,
                        "links":[
                        ]
                    }
                    """
                mock_request.data = json.loads(data)
                test = PersonViewSet()
                result = test.create(mock_request)
            assert result.status_code == 200 and result.data['Success'] > 1
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

