import unittest, sys, ast, io, os, json, copy
from google.cloud import datastore
 
class TestMainMethods(unittest.TestCase):
 
 
    def setUp(self):
        pass
 
 
    def tearDown(self):
       pass
        
  
    # Begin Tests   
    def test_build_teams(self):
        # call the build_teams method from 0 to max_player_count times with fictional player data
        max_player_count = 11 # zero indexed so it will only go this -1

        for i in range(max_player_count):
            print("Testing team size "+str(i))
            registrations = list()
            for j in range(i):
                entity = datastore.Entity()
                entity['name'] = "Player_"+str(j+1) 
                registrations.append(entity)
            teams = build_teams(registrations)
            print("Teams for team size "+str(i),teams)
        print (json.dumps(registrations))
 
def build_teams(registrations):
    team = list()
    teams = list()
 
    # handle the zero case
    if len(registrations) == 0:
       return teams

    # If the number of registrations is less than four, just add them and return
    if len(registrations) <= 4:
        for reg in registrations:
            team.append(reg['name'])
        teams.append(team)
        return teams
 
    reg_length = len(registrations)
    # print("Length of registration list: ",int(reg_length))
    
    for idx,reg in enumerate(registrations):
        
        if len(team) < 4:  # If length of team is less than four, add to team and continue
           team.append(reg['name'])
           # print("Case 1 ",str(reg_length), "Iteration: ", str(idx), "Team: ", team, "Teams: ", teams)  

        elif idx+1 == reg_length:  # Length of team is four also check if this is our last iteration, if so steal last from team to create new team
            team_member_swap = team[-1]
            team.pop()
            teams.append(team.copy())
            teams.append([team_member_swap,reg['name']])
            team = list()
            # print("Case 2",str(reg_length), "Iteration: ", str(idx), "Team: ", team, "Teams: ", teams)   

        else: # save the old team and start a new one with the current reg
            # print("Case 3a ",str(reg_length), "Iteration: ", str(idx), "Team: ", team, "Teams: ", teams)
            teams.append(team.copy())
            team = list()
            team.append(reg['name'])
            # print("Case 3b ",str(reg_length), "Iteration: ", str(idx), "Team: ", team, "Teams: ", teams)

    if len(team) > 0:
        teams.append(team.copy()) # add the last team created

    return teams


if __name__ == '__main__':
    unittest.main()
