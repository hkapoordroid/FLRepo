# [START app]
import logging
import urllib2
import csv
import StringIO
import ast

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
    tval = request.form['tval']
    mval = request.form['mval']
    rval = 100

    #read the csv file to get the adj close range
    csvfileurl = 'https://s3.eu-west-2.amazonaws.com/flelliotvar0/'+company+'.csv'
    print(csvfileurl)
    rcsv = urllib2.urlopen(csvfileurl)
    csvstream = StringIO.StringIO(rcsv.read())
    csvdata = list(csv.reader(csvstream))
    adj_close = [float(row[6]) for row in csvdata[1:]]




    if runat == 'lambda':
    	r = urllib2.urlopen('http://6pi4zde07i.execute-api.eu-west-2.amazonaws.com/Prod?company='+str(company)+'&investment='+str(investment)+'&rval=100&tval='+str(tval)+'&mval='+str(mval))
    else:
        r = urllib2.urlopen('http://ec2-35-176-60-162.eu-west-2.compute.amazonaws.com/?company='+str(company)+'&investment='+str(investment)+'&rval=100&tval='+str(tval)+'&mval='+str(mval))

    rdict = ast.literal_eval(r.read())

    # [END submitted]
    # [START render_template]
    return render_template(
        'result.html',
        historic95 = "%.2f" % rdict['historical'][0],
	historic99 = "%.2f" % rdict['historical'][1],
	covariance95 = "%.2f" % rdict['covariance'][0],
	covariance99 = "%.2f" % rdict['covariance'][1],
	montecarlo95 = "%.2f" % rdict['montecarlo'][0],
	montecarlo99 = "%.2f" % rdict['montecarlo'][1])
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]


