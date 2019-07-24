

# [START app]
import logging
import datetime
import socket
import config
import requests
import json

import model_datastore
from google.cloud import datastore

# [START imports]
from flask import Flask, render_template, request
# from google.cloud import datastore
# [END imports]

# Start app and configure it
app = Flask(__name__)
app.config.from_object(config)
app.debug = False
app.testing = False

# Configure logging
if not app.testing:
    logging.basicConfig(level=logging.INFO)



# [START default route]
@app.route('/')
def default():
    return render_template('main.html')
# [END form]

# [START form]
@app.route('/form')
def form():
    return render_template('form.html')
# [END form]


# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    

    name = request.form['name']
    email = request.form['email']
    participant_type = request.form['participant_type']
    timestamp = datetime.datetime.utcnow().isoformat()

    data = request.form.to_dict(flat=True)
    data['timestamp'] = timestamp
    print(data)
    app.logger.info(data)    
 
    model_datastore.update(data)


    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        participant_type=participant_type,
        timestamp=timestamp)
    # [END render_template]


# [START list]
@app.route("/list")
def submissions():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    app.logger.info("Getting list of results")
    regs, next_page_token = model_datastore.list(cursor=token)
    app.logger.info("received list of results")
    
    # teams = build_teams(regs)
    teams = call_gcp_build_teams(regs)
    print("teams type: {}".format(type(teams).__name__))
    app.logger.info("built teams list of results")

    return render_template(
        "list.html",
        registrations=regs,
        next_page_token=next_page_token,teams=teams)
# [END list]


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred', 500


def call_gcp_build_teams(registrations):
    url = 'https://us-central1-russels-playground.cloudfunctions.net/build_teams'
    players = list()
    for idx,reg in enumerate(registrations):
        players.append(reg['name'])
    
    jsonStr = '{\"players\": '+ json.dumps(players) + '}'
    print("calling gcp build_teams with: {}".format(jsonStr))
    response = requests.post(url, json=jsonStr)
    print("received response: {}".format(response.text))
    return response.json()

 # [START build_teams]
def build_teams(registrations):
    team = []
    teams = []
 
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
    
    for idx,reg in enumerate(registrations):
        
        if len(team) < 4:  # If length of team is less than four, add to team and continue
           team.append(reg['name'])

        elif idx+1 == reg_length:  # Length of team is four also check if this is our last iteration, if so steal last from team to create new team
            team_member_swap = team[-1]
            team.pop()
            teams.append(team.copy())
            teams.append([team_member_swap,reg['name']])
            team = []

        else: # save the old team and start a new one with the current reg
            # print("Case 3a ",str(reg_length), "Iteration: ", str(idx), "Team: ", team, "Teams: ", teams)
            teams.append(team.copy())
            team = []
            team.append(reg['name'])

    if len(team) > 0:
        teams.append(team.copy()) # add the last team created

    return teams
# [END build_teams]

if __name__ == "__main__":

    app.run(host='127.0.0.1', port=8080, debug=True)
