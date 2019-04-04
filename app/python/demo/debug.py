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

# python app\python\manage.py test plus.debug.MyTestCases.test<TestName> --settings admin.settings

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

    def testPublicationModel(self):
        try:
            import models
            publications = models.Publication.objects.filter(emdesk_phase='RUP')
            assert True
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testHomePage(self):
        print('Calling \'testHomePage\'')
        try:
            #mock_render_to_response = mock.MagicMock()
            with mock.patch.multiple( \
                'plus.views', \
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

    def testEditPage(self):
        print('Calling \'testEditPage\'')
        try:
            #mock_render_to_response = mock.MagicMock()
            with mock.patch.multiple( \
                'plus.views', \
                #render_to_response=mock_render_to_response, \ # Use a real 'render_to_response' and test the returned HttpResponse object instead
                RequestContext=mock.MagicMock(), \
                login_required=lambda x: x, \
                user_passes_test=lambda x: x \
                ):
                from views import edit
                mock_request = mock.Mock()
                mock_request.user.username = 'simon'
                result = edit(mock_request)
                #_, args, _ = mock_render_to_response.mock_calls[0] # Could examine the template data here
            assert result.status_code == 200
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testSubProjectPage(self):
        print('Calling \'testSubProjectPage\'')
        try:
            #mock_render_to_response = mock.MagicMock()
            with mock.patch.multiple( \
                'plus.views', \
                #render_to_response=mock_render_to_response, \ # Use a real 'render_to_response' and test the returned HttpResponse object instead
                RequestContext=mock.MagicMock(), \
                login_required=lambda x: x, \
                user_passes_test=lambda x: x \
                ):
                from views import the_subproject
                mock_request = mock.Mock()
                mock_request.user.username = 'simon'
                result = the_subproject(mock_request,'6')
                #_, args, _ = mock_render_to_response.mock_calls[0] # Could examine the template data here
            assert result.status_code == 200
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testOptimisedModels(self): # test plus.debug.MyTestCases.testOptimisedModels
        try:
            import optimisedModels
            test = optimisedModels.OptimisedModels()
            sqlStatement = \
                """
                select 
	                array_to_json(array_agg(row_to_json(full_results)))
                from 
	                (
	                select 
		                consortium.abbreviation as phase,
		                (
                        select 
                            array_to_json(array_agg(row_to_json(task_results)))
                        from
                            (
                            select 
	                            subproject.consortium_id as consortium_id,
	                            subproject.id as subproject_id,
	                            workpackage.id as workpackage_id,
                                task.id as task_id, 
	                            task.hbp_id as task_hbp_id,
	                            task.phase as task_phase,
	                            cast(substring(task.hbp_id from 'T(\d+)\.\d+\.\d+') as int) as task_sp,
	                            cast(substring(task.hbp_id from 'T\d+\.(\d+)\.\d+') as int) as task_wp,
	                            cast(substring(task.hbp_id from 'T\d+\.\d+\.(\d+)') as int) as task_t,
	                            task.pms as task_pms,
	                            contribution_summary.count as contribution_count,
	                            contribution_summary.pms as contribution_pms,
	                            (task.pms-contribution_summary.pms) as computed_pms_difference
                            from 
	                            public.plus_task task
	                            left outer join public.plus_workpackage workpackage
    	                            on task.workpackage_id=workpackage.id
	                            left outer join public.plus_subproject subproject
    	                            on workpackage.subproject_id=subproject.id
	                            left outer join 
        	                        (
				                    select 
        			                    task_id,
					                    count(*) as count,
                	                    sum(pms) as pms
				                    from 
    				                    public.plus_contribution
				                    group by
        			                    task_id
			                        ) contribution_summary
        	                            on contribution_summary.task_id=task.id
                            where
	                            task.phase=consortium.abbreviation
                            order by
	                            task_phase desc,
	                            task_wp,
	                            task_sp,
	                            task_t
                            ) task_results
		                ) as tasks
	                from
		                public.plus_consortium consortium
	                order by
		                phase desc
	                ) full_results
                """
            results = test.Execute(sqlStatement, lambda results: [u'{%s}'%u','.join([u'"consortium_id": "%s"'%unicode(str(v[u'consortium_id'])), u'"subproject_id": "%s"'%unicode(str(v[u'subproject_id'])), u'"workpackage_id": "%s"'%unicode(str(v[u'workpackage_id'])), u'"task_id": "%s"'%unicode(str(v[u'task_id'])), u'"task_hbp_id": "%s"'%unicode(str(v[u'task_hbp_id'])), u'"task_phase": "%s"'%unicode(str(v[u'task_phase'])), u'"task_sp": "%s"'%unicode(str(v[u'task_sp'])), u'"task_wp": "%s"'%unicode(str(v[u'task_wp'])), u'"task_t": "%s"'%unicode(str(v[u'task_t'])), u'"task_pms": "%s"'%unicode(str(v[u'task_pms'])), u'"contribution_count": "%s"'%unicode(str(v[u'contribution_count'])), u'"contribution_pms": "%s"'%unicode(str(v[u'contribution_pms'])), u'"computed_pms_difference": "%s"'%unicode(str(v[u'computed_pms_difference']))]) for i,v in enumerate(results)]) # Executes the SQL and uses the lambda to build the list
            print results
            assert True
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testComponentQuery(self):
        try:
            import componentQuery
            test = componentQuery.ComponentQuery('component')
            results = test.Execute('{"Criteria": {"Type": null, "FundingPeriod": "SGA1", "SubProject": "5", "WorkPackage": "5.4", "Task": "5.4.1", "Keywords": []}}')
            assert True
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testComponentQueryGet(self): # test plus.debug.MyTestCases.testComponentQueryGet
        print('Calling \'testComponentQueryGet\'')
        try:
            import componentQuery
            test = componentQuery.ComponentQuery('component')
            results = test.get('{"Criteria": {"Component_date": null, "sub_project": "SP7", "phase": null, "keywords": [], "author": null, "Component": null}}')
            self.assertTrue((re.search(r'Components', str(results)) != None), r'Unexpected contents')
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testComponentQuerySet(self): # test plus.debug.MyTestCases.testComponentQuerySet
        print('Calling \'testComponentQuerySet\'')
        try:
            import componentQuery
            test = componentQuery.ComponentQuery('component')
            payload = \
                """
                {
                    "id": 30,
                    "name": "My first component",
                    "description": "The first component I ever made!",
                    "type_of_component": 1,
                    "classification": 3,
                    "trl": 4,
                    "implementation_leader": "Simon",
                    "implementation_team": "Florian,Benoit",
                    "ip_license": 32,
                    "privacy_constraints": 2,
                    "release_plan": "Quick & dirty",
                    "repository_url": "https://plus.humanbrainproject.org/",
                    "users": "Everyone",
                    "links": [
                        {"name": "T1.1.1","value": 633,"type": 4},
                        {"name": "T1.1.3","value": 635,"type": 4}
                    ],
                    "releases": [
                        {
                        "id": 0,
                        "name": "cobalt",
                        "description": "v1",
                        "target_date": "2018-08-02",
                        "target_trl": 9,
                        "effective_date": "2018-10-12",
                        "effective_trl": 7,
                        "accepted_date": "2018-12-23",
                        "repository_id": 0,
                        "links": [
                            {"name": "T4.3.3","value": 730,"type": 4},
                            {"name": "T2.4.2","value": 822,"type": 4}
                        ],
                        "features": [
                            {
                            "id": 0,
                            "name": "First feature",
                            "description": "lorem ipsum dolor sit amet"
                            },
                            {
                            "id": 0,
                            "name": "Second feature",
                            "description": "consectetur adipiscing elit"
                            },
                            {
                            "id": 0,
                            "name": "Third feature",
                            "description": "phasellus vel maximus mauris"
                            }
                        ]
                        },
                        {
                        "id": 0,
                        "name": "iridium",
                        "description": "v2",
                        "target_date": "2019-03-02",
                        "target_trl": 6,
                        "effective_date": "2019-05-12",
                        "effective_trl": 3,
                        "accepted_date": "2019-08-23",
                        "repository_id": 0,
                        "links": [
                            {"name": "T4.3.3","value": 730,"type": 4},
                            {"name": "T2.4.2","value": 822,"type": 4}
                        ],
                        "features": [
                            {
                            "id": 0,
                            "name": "Fourth feature",
                            "description": "more Latin"
                            },
                            {
                            "id": 0,
                            "name": "Fifth feature",
                            "description": "yet more Latin"
                            },
                            {
                            "id": 0,
                            "name": "Sixth feature",
                            "description": "and even more Latin"
                            }
                        ]
                        }
                    ]
                }
                """
            result = test.set(json.loads(payload), 'simon')
            self.assertTrue((re.search(r'Success', str(result)) != None), r'Unexpected contents')
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testPublicationQueryGet(self): # test plus.debug.MyTestCases.testPublicationQueryGet
        print('Calling \'testPublicationQueryGet\'')
        try:
            import publicationQuery
            test = publicationQuery.PublicationQuery('publication')
            results = test.get('{"Criteria": {"publication_date": null, "sub_project": "SP7", "phase": null, "keywords": [], "author": null, "publication": null}}')
            self.assertTrue((re.search(r'Publications', str(results)) != None), r'Unexpected contents')
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testPublicationQuerySet(self): # test plus.debug.MyTestCases.testPublicationQuerySet
        print('Calling \'testPublicationQuerySet\'')
        try:
            import publicationQuery
            test = publicationQuery.PublicationQuery('publication')
            payload = \
                """
                {
                    "id":101202,
                    "doi":"10.15252/embr.201744696",
                    "title":"A really new test title",
                    "publication_date":"2017-07-25",
                    "publication_url":"http://onlinelibrary.wiley.com/doi/10.15252/embr.201744696/full",
                    "type_of_publication":1,
                    "open_access":3,
                    "acknowledgement_text":"Powered by HBP",
                    "publisher":"Elsevier",
                    "publication":"Cell",
                    "ranked_authors":"Markram",
                    "links":[
                        {"name":"T1.1.1","value":633},
                        {"name":"T1.1.3","value":635}
                    ]
                }
                """
            result = test.set(json.loads(payload), 'simon')
            self.assertTrue((re.search(r'Success', str(result)) != None), r'Unexpected contents')
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testPublicationViewSetCreate(self): # test plus.debug.MyTestCases.testPublicationViewSet
        print('Calling \'testPublicationViewSetCreate\'')
        try:
            import publicationViewSet
            #mock_render_to_response = mock.MagicMock()
            with mock.patch('plus.publicationViewSet'):
                mock_request = mock.Mock()
                mock_request.body = \
                    """
                    {
                        "id":101193,
                        "doi":"10.15252/embr.201744696",
                        "title":"A really new test title",
                        "publication_date":"2017-07-25",
                        "publication_url":"http://onlinelibrary.wiley.com/doi/10.15252/embr.201744696/full",
                        "type_of_publication":1,
                        "open_access":3,
                        "acknowledgement_text":"Powered by HBP",
                        "publisher":"Elsevier",
                        "publication":"Cell",
                        "ranked_authors":"Markram",
                        "links":[
                            {"name":"T1.1.1","value":633},
                            {"name":"T1.1.3","value":635}
                        ]
                    }
                    """
                test = publicationViewSet.PublicationViewSet()
                result = test.create(mock_request)
                #_, args, _ = mock_render_to_response.mock_calls[0] # Could examine the template data here
            assert result.status_code == 200 and result.data[u'Success'] > 1
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testEventQueryGet(self): # test plus.debug.MyTestCases.testEventQueryGet
        print('Calling \'testEventQueryGet\'')
        try:
            import eventQuery
            test = eventQuery.EventQuery('event')
            results = test.get('{"Criteria": {"start_date": null}}')
            self.assertTrue((re.search(r'Events', str(results)) != None), r'Unexpected contents')
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testEventQuerySet(self): # test plus.debug.MyTestCases.testEventQuerySet
        print('Calling \'testEventQuerySet\'')
        try:
            import eventQuery
            test = eventQuery.EventQuery('event')
            payload = \
                """
                {
                    "id":0,
                    "title":"The very first event",
                    "start_date":"20180612",
                    "start_time":"0900",
                    "end_date":"20180612",
                    "end_time":"1700",
                    "organiser":"Simon",
                    "location":"Geneva",
                    "description":"An event to discuss the benefits of Django",
                    "registration_date":"20180412",
                    "registration_url":"www.epfl.ch/register",
                    "event_url":"www.epfl.ch/event",
                    "image_url":"",
                    "type_of_event":3,
                    "channel":100,
                    "goals":"To see if it works!",
                    "results":"",
                    "audience":0,
                    "collab_url":"",
                    "has_fee":false,
                    "size":1000,
                    "links":[
                        {"name":"SP5","value":32}
                    ]
                }
                """
            result = test.set(json.loads(payload), 'simon')
            self.assertTrue((re.search(r'Success', str(result)) != None), r'Unexpected contents')
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testDisseminationPlanQuerySet(self): # test plus.debug.MyTestCases.testDisseminationPlanQuerySet
        print('Calling \'testDisseminationPlanQuerySet\'')
        try:
            import disseminationPlanQuery
            test = disseminationPlanQuery.DisseminationPlanQuery('dissemination_plan')
            payload = \
                """
                {
                    "description": "State-of-the-art curation workflow leading to world-class data quality",
                    "links": [],
                    "sub_project": "SP6",
                    "tagline": "Pushing the boundaries...",
                    "saved_by": "simon",
                    "positioning": [
                        {
                        "audience": "Neuroscientists",
                        "message": "Use me!",
                        "id": 9
                        },
                        {
                        "audience": "",
                        "message": "",
                        "id": 10
                        },
                        {
                        "audience": "",
                        "message": "",
                        "id": 11
                        },
                        {
                        "audience": "",
                        "message": "",
                        "id": 12
                        }
                    ],
                    "dissemination_goals": "Spread the word...worldwide!",
                    "positioning_statement": "Make HBP the #1 resource for brains",
                    "programme": [
                        {
                        "impact": "Big",
                        "supporting_channel": "TV",
                        "primary_channel": "Web",
                        "audience": "Everyone",
                        "by_when": "8-18",
                        "partner": "All",
                        "key_result": "Take-up",
                        "id": 9
                        },
                        {
                        "impact": "",
                        "supporting_channel": "",
                        "primary_channel": "",
                        "audience": "",
                        "by_when": "",
                        "partner": "",
                        "key_result": "",
                        "id": 10
                        },
                        {
                        "impact": "",
                        "supporting_channel": "",
                        "primary_channel": "",
                        "audience": "",
                        "by_when": "",
                        "partner": "",
                        "key_result": "",
                        "id": 11
                        },
                        {
                        "impact": "",
                        "supporting_channel": "",
                        "primary_channel": "",
                        "audience": "",
                        "by_when": "",
                        "partner": "",
                        "key_result": "",
                        "id": 12
                        }
                    ],
                    "id": 7,
                    "saved_on": "2018-08-14T12:50:57.672107+02:00"
                }
                """
            result = test.set(json.loads(payload), 'simon')
            self.assertTrue((re.search(r'Success', str(result)) != None), r'Unexpected contents')
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testTaskOverview(self):
        try:
            import taskOverview
            test = taskOverview.TaskOverview()
            results = test.Execute()
            assert True
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testComponentQueryPage(self):
        print('Calling \'testComponentQueryPage\'')
        try:
            #mock_render_to_response = mock.MagicMock()
            with mock.patch.multiple( \
                'plus.views', \
                #render_to_response=mock_render_to_response, \ # Use a real 'render_to_response' and test the returned HttpResponse object instead
                RequestContext=mock.MagicMock(), \
                login_required=lambda x: x, \
                user_passes_test=lambda x: x \
                ):
                from views import query_components
                mock_request = mock.Mock()
                mock_request.body = '{"Criteria": {"Type": null, "FundingPeriod": "SGA1", "SubProject": "5", "WorkPackage": "5.4", "Task": "5.4.1", "Keyword": []}}'
                result = query_components(mock_request)
                #_, args, _ = mock_render_to_response.mock_calls[0] # Could examine the template data here
            print result.content
            assert result.status_code == 200 and result.content.find(r'Components') != -1
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testTaskOverviewPage(self):
        print('Calling \'testTaskOverviewPage\'')
        try:
            #mock_render_to_response = mock.MagicMock()
            with mock.patch.multiple( \
                'plus.views', \
                #render_to_response=mock_render_to_response, \ # Use a real 'render_to_response' and test the returned HttpResponse object instead
                RequestContext=mock.MagicMock(), \
                login_required=lambda x: x, \
                user_passes_test=lambda x: x \
                ):
                from views import tasks_overview_2dtable
                mock_request = mock.Mock()
                mock_request.body = ''
                result = tasks_overview_2dtable(mock_request)
                #_, args, _ = mock_render_to_response.mock_calls[0] # Could examine the template data here
            print result.content
            assert result.status_code == 200 and result.content.find(r'Tasks') != -1
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testScientificPublications(self):
        print('Calling \'testScientificPublications\'')
        try:
            #mock_render_to_response = mock.MagicMock()
            with mock.patch.multiple( \
                'plus.views', \
                #render_to_response=mock_render_to_response, \ # Use a real 'render_to_response' and test the returned HttpResponse object instead
                RequestContext=mock.MagicMock(), \
                login_required=lambda x: x, \
                user_passes_test=lambda x: x \
                ):
                from views import scientific_publications
                mock_request = mock.Mock()
                #mock_request.body = '{"Criteria": {"Type": null, "FundingPeriod": "SGA1", "SubProject": "5", "WorkPackage": "5.4", "Task": "5.4.1", "Keyword": []}}'
                result = scientific_publications(mock_request)
                #_, args, _ = mock_render_to_response.mock_calls[0] # Could examine the template data here
            print result.content
            assert result.status_code == 200 and result.content.find(r'Components') != -1
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testAllPublications(self):
        print('Calling \'testAllPublications\'')
        try:
            #mock_render_to_response = mock.MagicMock()
            with mock.patch.multiple( \
                'plus.views', \
                #render_to_response=mock_render_to_response, \ # Use a real 'render_to_response' and test the returned HttpResponse object instead
                RequestContext=mock.MagicMock(), \
                login_required=lambda x: x, \
                user_passes_test=lambda x: x \
                ):
                from views import all_publications
                mock_request = mock.Mock()
                result = all_publications(mock_request)
                #_, args, _ = mock_render_to_response.mock_calls[0] # Could examine the template data here
            print result.content
            assert result.status_code == 200 and result.content.find(r'Components') != -1
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testGetPublications(self):
        print('Calling \'testGetPublications\'')
        try:
            ##mock_render_to_response = mock.MagicMock()
            #with mock.patch.multiple( \
            #    'plus.views', \
            #    #render_to_response=mock_render_to_response, \ # Use a real 'render_to_response' and test the returned HttpResponse object instead
            #    RequestContext=mock.MagicMock(), \
            #    login_required=lambda x: x, \
            #    user_passes_test=lambda x: x \
            #    ):
            #    from views import get_publications
            #    mock_request = mock.Mock()
            #    result = get_publications(mock_request)
            #    #_, args, _ = mock_render_to_response.mock_calls[0] # Could examine the template data here
            #print result.content
            #assert result.status_code == 200 and result.content.find(r'Components') != -1
            client = Client()
            #url = '/v1/publications'
            #url = '/publications'
            url = '/plus/publications/'
            #url = '/'
            response = client.get(url)
            print('status_code: ' + str(response.status_code))
            self.assertTrue((re.search(r'Pub', str(response)) != None), r'Unexpected contents')
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testPubInfo(self):
        print('Calling \'testPubInfo\'')
        try:
            from views import get_info_no_phase
            results = get_info_no_phase()
            assert len(results) > 0
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testPublicationsForNewsletter(self):
        try:
            import publicationsForNewsletter
            # {"Criteria": {"Date": null, "FundingPeriod": "RUP", "Type": null, "Keywords": "Neocortical Microcircuitry", "FirstName": null, "LastName": null, "JournalURL": null}}
            publications = publicationsForNewsletter.PublicationsForNewsletter('{"Criteria": {"Date": null, "FundingPeriod": "RUP", "Type": null, "Keywords": null, "FirstName": null, "LastName": "Markram", "JournalURL": null}}')
            publicationsXML = publications.ExportAsXML()
            with open("publications.xml", "w") as file:
                file.write(publicationsXML.encode('utf8'))
            assert True
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testWebsitePublicationViewSet(self): # test plus.debug.MyTestCases.testWebsitePublicationViewSet
        print('Calling \'testWebsitePublicationViewSet\'')
        try:
            import websitePublicationViewSet
            test = websitePublicationViewSet.WebsitePublicationViewSet()
            publications = test.get_data('{"Criteria": {}}')
            assert True
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testGetAssociations(self): # test plus.debug.MyTestCases.testGetAssociations
        print('Calling \'testGetAssociations\'')
        try:
            #mock_render_to_response = mock.MagicMock()
            with mock.patch.multiple( \
                'plus.views', \
                #render_to_response=mock_render_to_response, \ # Use a real 'render_to_response' and test the returned HttpResponse object instead
                RequestContext=mock.MagicMock(), \
                login_required=lambda x: x, \
                user_passes_test=lambda x: x \
                ):
                from views import get_associations
                mock_request = mock.Mock()
                result = get_associations(mock_request)
            print result.content
            assert result.status_code == 200
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testGetPartners(self): # test plus.debug.MyTestCases.testGetPartners
        print('Calling \'testGetPartners\'')
        try:
            #mock_render_to_response = mock.MagicMock()
            with mock.patch.multiple( \
                'plus.views', \
                #render_to_response=mock_render_to_response, \ # Use a real 'render_to_response' and test the returned HttpResponse object instead
                RequestContext=mock.MagicMock(), \
                login_required=lambda x: x, \
                user_passes_test=lambda x: x \
                ):
                from views import get_partners
                mock_request = mock.Mock()
                result = get_partners(mock_request)
            print result.content
            assert result.status_code == 200
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testGetTasksComponents(self): # test plus.debug.MyTestCases.testGetTasksComponents
        print('Calling \'testGetTasksComponents\'')
        try:
            #mock_render_to_response = mock.MagicMock()
            with mock.patch.multiple( \
                'plus.views', \
                #render_to_response=mock_render_to_response, \ # Use a real 'render_to_response' and test the returned HttpResponse object instead
                RequestContext=mock.MagicMock(), \
                login_required=lambda x: x, \
                user_passes_test=lambda x: x \
                ):
                from views import get_tasks_components
                mock_request = mock.Mock()
                result = get_tasks_components(mock_request)
            print result.content
            assert result.status_code == 200
        except Exception as e:
            assert False,'Exception: %s'%str(e)

    def testGetDataJSON(self): # test plus.debug.MyTestCases.testGetDataJSON
        print('Calling \'testGetDataJSON\'')
        try:
            from views import get_data_json
            result = get_data_json('plus__definition', 'label,numeric', 'category=\'EntityType\'', None)
            if result[0]:
                print result[1]
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

