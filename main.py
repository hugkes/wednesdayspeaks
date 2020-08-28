from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pyttsx3
from queue import Queue
import os
from threading import Thread
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from logic import *

# Config
app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"\database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
q = Queue()
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["3 per minute"]
)
# Creates db (note subsequent runs will not re-create)
db.create_all()

# Renders the generic homepage
@app.route("/")
def homepage():
    return render_template("page.html", title="HOME PAGE")

# Kicks off logic when request made, renders message
@app.route('/', methods=['POST'])
def request_made():
    va = VoiceAssistant()
    va.start()
    text = request.form['text']
    user = request.form['user']
    db.session.add(Table(username=user, text_request = text))
    db.session.commit()
    message = ''
    text = "um" + text
    if "hate" in text:
        text = "I hate Anna"
    if len(text) < 250 and len(text.split()) < 40:
        va.add_say(text)
        message = "thanks bbg"
    else:
        message = "Requested speech is too long. Please shorten your message."
    va.q.join() # ends the loop when queue is empty
    return render_template("page.html", title="speaktowen", message = message)

# Renders the request history page
@app.route('/requests_log', methods=['GET','POST'])
def get_table_data():
    data = db.session.query(Table.id, Table.username, Table.text_request).order_by(Table.id.desc()).limit(5)
    return render_template('requests_log.html',  data = data)

if __name__ == "__main__":
    app.run()