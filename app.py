from flask import Flask, redirect, url_for, render_template, session, request
from flask_pymongo import PyMongo
from flask_oauthlib.client import OAuth
from functools import wraps
import os
from dotenv import load_dotenv
load_dotenv()

from GenerateVideo import GenerateVideo

MONGODB_URI          = os.environ.get('MONGODB_URI') 
GOOGLE_CLIENT_ID     = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') 

app = Flask(__name__)

# Configure MongoDB
app.config['MONGO_URI'] = MONGODB_URI
mongo = PyMongo(app)

# Configure Google OAuth
app.secret_key = 'LearnMateProject#@6666'
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=os.environ.get('GOOGLE_CLIENT_ID', GOOGLE_CLIENT_ID),
    consumer_secret=os.environ.get('GOOGLE_CLIENT_SECRET', GOOGLE_CLIENT_SECRET),
    request_token_params={
        'scope': 'email profile',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'google_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def login_page():
    if 'google_token' in session:
        return redirect('/dashboard')
    else:
        return render_template('index.html')

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect('/')

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@app.route('/login/authorized')
def authorized():
    token = google.authorized_response()

    if 'error' in token:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (token['access_token'], '')
    user_info = google.get('userinfo')
    user_id = user_info.data['id']

    # Check if user entry exists in the database
    user_entry = mongo.db.users.find_one({'user_id': user_id})

    if user_entry:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('academics'))

@app.route('/academics', methods=['GET', 'POST'])
def academics():
    if 'google_token' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Save the academic information to the database

        """"
        College
        Degree
        Year
        College_Name/School_Name  
        """

        college = request.form['college']

        class_year = request.form['class_year']
        board = request.form['board']

        user_info = google.get('userinfo')
        user_id = user_info.data['id']

        # Save the academic information to the database
        mongo.db.users.insert_one({'user_id': user_id, 'college': college, 'class_year': class_year, 'board': board})

        return redirect(url_for('dashboard'))

    return render_template('academics.html')

@app.route('/dashboard')
def dashboard():
    if 'google_token' not in session:
        return redirect(url_for('index'))

    user_info = google.get('userinfo')
    user_id = user_info.data['id']

    # Retrieve user information from the database
    user_entry = mongo.db.users.find_one({'user_id': user_id})

    videogen = GenerateVideo("photosynthesis")
    data_json = videogen.start()

    # Render the dashboard template with user information
    return render_template('dashboard.html', user_entry=user_entry, data=data_json)

if __name__ == '__main__':
    app.run(debug=True)
