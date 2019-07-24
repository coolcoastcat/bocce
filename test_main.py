import unittest, sys, ast, io, os, json, copy
from google.cloud import datastore
import cloud_functions.build_teams as bt
import flask
 
class TestMainMethods(unittest.TestCase):
 
 
    def setUp(self):
        pass
 
 
    def tearDown(self):
       pass
        
  
    # Begin Tests  
    
    def test_build_teams(self):
        app = flask.Flask(__name__)
        players = {"players":["Player1","Player2","Player3","Player4","Player5","Player6","Player7","Player8","Player9","Player10","Player11"]}
        with app.test_request_context(players):
            bt.build_teams()
 
 

if __name__ == '__main__':
    unittest.main()
