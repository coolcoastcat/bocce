

# [START app]
import logging
import datetime
import socket
import config

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
    timestamp = datetime.datetime.utcnow()

    data = request.form.to_dict(flat=True)
    data['timestamp'] = unicode(timestamp)
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


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)