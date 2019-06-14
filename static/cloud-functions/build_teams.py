import json

# [START build_teams]
def build_teams(request):
    team = []
    teams = []
 
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'name' in request_json:
            name = request_json['name']
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    elif content_type == 'application/octet-stream':
        raise ValueError("received application/octet-stream content instead of JSON")
    elif content_type == 'text/plain':
        raise ValueError("received text/plain content instead of JSON")
    elif content_type == 'application/x-www-form-urlencoded':
        raise ValueError("received POSTed content instead of JSON")
    else:
        raise ValueError("Unknown content type: {}".format(content_type))
    
    # Requests should contain JSON
    request_json = request.get_json(silent=True)

    if not request_json or 'players' not in request_json:
        return json.dumps(teams)

    players_list = request.players

    # handle the zero case
    if len(players_list) == 0:
       return json.dumps(teams)

    # If the number of registrations is less than four, just add them and return
    if len(players_list) <= 4:
        for player in players_list:
            team.append(player)
        teams.append(team)
        return json.dumps(teams)
 
    reg_length = len(players_list)
    
    for idx,player in enumerate(players_list):
        
        if len(team) < 4:  # If length of team is less than four, add to team and continue
           team.append(player)

        elif idx+1 == reg_length:  # Length of team is four also check if this is our last iteration, if so steal last from team to create new team
            team_member_swap = team[-1]
            team.pop()
            teams.append(team.copy())
            teams.append([team_member_swap,player])
            team = []

        else: # save the old team and start a new one with the current reg
            # print("Case 3a ",str(reg_length), "Iteration: ", str(idx), "Team: ", team, "Teams: ", teams)
            teams.append(team.copy())
            team = []
            team.append(player)

    if len(team) > 0:
        teams.append(team.copy()) # add the last team created

    return json.dumps(teams)
# [END build_teams]