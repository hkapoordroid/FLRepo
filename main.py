# [START app]
import logging
import urllib2

# [START imports]
from flask import Flask, render_template, request
# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]


# [START form]
@app.route('/')
def form():
    return render_template('form.html',result="")
# [END form]


# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    company = request.form['company']
    investment = request.form['investment']
    runat = request.form['runat']

    if runat == 'lambda':
    	r = urllib2.urlopen('http://6pi4zde07i.execute-api.eu-west-2.amazonaws.com/Prod?company='+str(company)+'&investment='+str(investment))
    else:
        r = urllib2.urlopen('http://ec2-35-177-240-17.eu-west-2.compute.amazonaws.com/?company='+str(company)+'&investment='+str(investment))


    # [END submitted]
    # [START render_template]
    return render_template(
        'form.html',
        result=r.read())
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]


