from flask import Flask, redirect, url_for, render_template, session, request, jsonify
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
ELEVEN_LABS_API      = os.environ.get('ELEVEN_LABS_API')

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
        return redirect(url_for('dashboard', topic='Photosynthesis'))
    else:
        return redirect(url_for('academics'))

@app.route('/academics', methods=['GET', 'POST'])
def academics():
    if 'google_token' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        user_info = google.get('userinfo')
        user_id = user_info.data['id']
        email   = user_info.data['email']
        picture = user_info.data['picture']
        name    = user_info.data['name']

        educationType = request.form['educationType'] # Collge/School
        if educationType == "college":
            stream  = request.form['stream']  # B.tect/BSC
            course  = request.form['course']  # CS/IT/ECE
            year    = request.form['year']    # 1/2/3/4
            college_name = request.form['college_name']

            print("educationType: ", educationType)
            print("stream: ", stream)
            print("course: ", course)
            print('college_name: ', college_name)

            # Save the academic information to the database
            mongo.db.users.insert_one({
                'user_id': user_id, 
                'email': email,
                'picture': picture,
                'name': name, 
                'rank': mongo.db.users.count_documents({}) + 1, 
                'hours_spend': 0,

                'educationType': educationType, 
                'stream': stream, 
                'course': course,
                'year': year,
                'college_name': college_name,
            })

        else:
            class_name = request.form['class']
            board      = request.form['board']

            print("class_name: ", class_name)
            print("board: ", board)

            # Save the academic information to the database
            mongo.db.users.insert_one({
                'user_id': user_id, 
                'email': email,
                'picture': picture,
                'name': name, 
                'rank': mongo.db.users.count_documents({}) + 1, 
                'hours_spend': 0,

                'educationType': educationType, 
                'class_name': class_name, 
                'board': board,
            })

        return redirect(url_for('dashboard', topic='Photosynthesis'))

    return render_template('academics.html')

@app.route('/dashboard')
def dashboard():
    if 'google_token' not in session:
        return redirect(url_for('login'))

    try:
        user_info = google.get('userinfo')
        user_id = user_info.data['id']
    except:
        return redirect(url_for('logout'))
    
    topic = request.args.get('topic', default='Rain Water Harvestation')

    course_curriculum = {
        "Photosynthesis": ["Definition of Photsynthesis", "Chlorophyll"],
        "Animal Cell": ["Definition of Photsynthesis", "Chlorophyll"],
        "Plant Cell": ["Definition of Photsynthesis", "Chlorophyll"],
        "Human Organ Systems": ["Definition of Photsynthesis", "Chlorophyll"],
        "Respiration in Humans": ["Definition of Photsynthesis", "Chlorophyll"],
    }

    # Retrieve user information from the database
    user_entry = mongo.db.users.find_one({'user_id': user_id})
    return render_template('dashboard.html', user_entry=user_entry, topic=topic, course_curriculum=course_curriculum)

@app.route('/api/generate_video')
def generate_video_api():
    topic = request.args.get('topic', default='Photosynthesis')

    # Generate video data based on the topic
    videogen = GenerateVideo(topic, ELEVEN_LABS_API)
    data_json = videogen.start()
    scene_length = len(data_json)

    return jsonify({'data_json': data_json, 'scene_length': scene_length})

@app.route('/api/generate_quiz')
def generate_quiz_api():
    topic = request.args.get('topic', default='Photosynthesis')

    # Generate video data based on the topic
    videogen = GenerateVideo(topic)
    data_json = videogen.start()
    scene_length = len(data_json)

    return jsonify({'data_json': data_json, 'scene_length': scene_length})

if __name__ == '__main__':
    app.run(debug=True)
