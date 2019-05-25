from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from random import choice
import logging
import pytz

app = Flask(__name__)

# Let's store stuff in sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# Set up logging
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)

# Define which Homer Simpson images are available
homer_images = ['static/homer1.png', 'static/homer2.png']


# One table for visits to /homersimpson endpoint
class HomerVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)

    def __init__(self):
        self.count = 0


# One table for visits to /covilha endpoint
class CovilhaVisit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)

    def __init__(self):
        self.count = 0


# Initialize DB
db.create_all()


# The default route with the default output
@app.route('/')
def hello():
    return "Hello World!"


# Add the /homersimpson endpoint
# Check if we have anything in the DB, if not set it up
# If there's something there, just increment
@app.route('/homersimpson')
def homersimpson():
    v = HomerVisit.query.first()
    if not v:
        v = HomerVisit()
        v.count += 1
        db.session.add(v)
    else:
        v.count += 1
    db.session.commit()

    homer_image = choice(homer_images)
    return render_template('homer.html', url=homer_image)


# Add the /covilha endpoint
# Check if we have anything in the DB, if not set it up
# If there's something there, just increment
@app.route('/covilha')
def covilha():
    v = CovilhaVisit.query.first()
    if not v:
        v = CovilhaVisit()
        v.count += 1
        db.session.add(v)
    else:
        v.count += 1
    db.session.commit()

    tz_covilha = pytz.timezone("Portugal")
    dt_covilha = datetime.now(tz_covilha).strftime("%H:%M:%S")
    return "The time in Covilha, Portugal is %s\n" % (dt_covilha)


# Set up the /metrics route
# FIXME: better formating for multiline string
@app.route('/metrics')
def metrics():
    hn = HomerVisit.query.first()
    cn = CovilhaVisit.query.first()

    if not hn:
        homer_number = 0
    else:
        homer_number = hn.count

    if not cn:
        covilha_number = 0
    else:
        covilha_number = cn.count

    output = "\
# HELP homer_http_requests_total The total number of HTTP requests for \
/homersimpson endpoint\n\
# TYPE homer_http_requests_total counter\n\
homer_http_requests_total{method=\"get\"} %s\n\
# HELP covilha_http_requests_total The total number of HTTP \
requests for /covilha endpoint\n\
# TYPE covilha_http_requests_total counter\n\
covilha_http_requests_total{method=\"get\"} %s\n" % \
        (homer_number, covilha_number)

    return(output)


# Set up the /healthz route
# FIXME: better and/or more thorough way to check if everything's OK
@app.route('/healthz')
def health():
    return "OK", 200


# Return the application version on /version
@app.route('/version')
def version():
    return "1.0.0\n", 200


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0')
