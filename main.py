

# [START app]
import logging
import datetime
import socket

# [START imports]
from flask import Flask, render_template, request
# from google.cloud import datastore
# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]


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

 #   ds = datastore.Client()

    name = request.form['name']
    email = request.form['email']
    participant_type = request.form['participant_type']
    timestamp = datetime.datetime.utcnow()

    # entity = datastore.Entity(key=ds.key('registration'))
    # entity.update({
    #     'user_name': name,
    #     'email': email,
    #     'participant_type': participant_type,
    #     'timestamp': timestamp
    # })

    # ds.put(entity)


    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        participant_type=participant_type,
        timestamp=timestamp)
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]