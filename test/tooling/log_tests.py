#TO RUN: joey2 project_operation_tests.py
import os
import sys
import unittest
import mock
import shutil
sys.path.append('../')
sys.path.append('../../')
import lib.mm_util as mm_util
import test_util as util
import test_helper
from test_helper import MavensMateTest
import mm    
import lib.mm_client as sfdc

base_test_directory = os.path.dirname(os.path.dirname(__file__))

class StackTraceAndLogsTest(MavensMateTest):
    
    def test_01_new_debug_log(self): 
        test_helper.create_project("unit test tooling project")
        commandOut = self.redirectStdOut()
        stdin = {
            "project_name"      : "unit test tooling project",
            "type"              : "user",
            "debug_categories"  : {
                "ApexCode"      : "DEBUG",
                "Visualforce"   : "INFO"
            }
        }
        mm_util.get_request_payload = mock.Mock(return_value=stdin)
        sys.argv = ['mm.py', '-o', 'new_log']
        mm.main()
        mm_response = commandOut.getvalue()
        sys.stdout = self.saved_stdout
        #print mm_response
        mm_json_response = util.parse_mm_response(mm_response)
        self.assertTrue(mm_json_response['success'] == True)
        self.assertTrue('id' in mm_json_response and len(mm_json_response['id']) is 18)

    def test_02_new_quicklog(self): 
        commandOut = self.redirectStdOut()
        stdin = {
            "project_name"      : "unit test tooling project",
            "type"              : "user",
            "debug_categories"  : {
                "ApexCode"      : "DEBUG",
                "Visualforce"   : "INFO"
            }
        }
        mm_util.get_request_payload = mock.Mock(return_value=stdin)
        sys.argv = ['mm.py', '-o', 'new_quick_log']
        mm.main()
        mm_response = commandOut.getvalue()
        sys.stdout = self.saved_stdout
        #print mm_response
        mm_json_response = util.parse_mm_response(mm_response)
        self.assertTrue(mm_json_response['success'] == True)
        self.assertTrue('1 Log(s) created successfully' in mm_json_response['body'])

    def test_03_update_debug_settings(self): 
        commandOut = self.redirectStdOut()
        stdin = {
            "project_name"      : "unit test tooling project",
            "debug_categories"  : {
                "Workflow"      : "FINE", 
                "Callout"       : "FINE", 
                "System"        : "FINE", 
                "Database"      : "FINE", 
                "ApexCode"      : "FINE", 
                "Validation"    : "FINE", 
                "Visualforce"   : "FINE"
            },
            "expiration"        : 120
        }
        mm_util.get_request_payload = mock.Mock(return_value=stdin)
        sys.argv = ['mm.py', '-o', 'update_debug_settings']
        mm.main()
        mm_response = commandOut.getvalue()
        sys.stdout = self.saved_stdout
        #print mm_response
        mm_json_response = util.parse_mm_response(mm_response)
        new_debug_settings = util.parse_json_file(os.path.join(base_test_directory, "test_workspace", stdin["project_name"], "config", ".debug"))
        self.assertTrue(new_debug_settings['expiration'] == stdin["expiration"])
        self.assertTrue(new_debug_settings['levels']['Workflow'] == stdin["debug_categories"]["Workflow"])
        self.assertTrue(new_debug_settings['levels']['Visualforce'] == stdin["debug_categories"]["Visualforce"])

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test tooling project")):
           shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test tooling project"))
        #pass

if __name__ == '__main__':
    if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test tooling project")):
        shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test tooling project"))
    unittest.main()