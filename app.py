from flask import Flask, redirect, url_for, render_template, session
from flask_pymongo import PyMongo
from flask_oauthlib.client import OAuth

app = Flask(__name__)

# Configure MongoDB
app.config['MONGO_URI'] = 'your_mongo_uri'
mongo = PyMongo(app)

# Configure Google OAuth
app.secret_key = 'your_secret_key'
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key='your_google_consumer_key',
    consumer_secret='your_google_consumer_secret',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def index():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (resp['access_token'], '')
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

    # Render the dashboard template with user information
    return render_template('dashboard.html', user_entry=user_entry)

if __name__ == '__main__':
    app.run(debug=True)
