from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import time
import win32com.client as wincl
import pythoncom
from logic import *

# Config
app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"\database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["3 per minute"]
)

# Renders the homepage
@app.route("/")
def homepage():
    return render_template("page.html", title="HOME PAGE")

# Initiates logic on request
@app.route('/', methods=['GET', 'POST'])
def add_request():
    hr = HandleRequest()
    va = VoiceAssistant()
    text = request.form['text']
    user = request.form['user']
    message = hr.add_db_msg(user, text)
    va.say(text)
    return render_template("page.html", title="add_request", message = message)

# Renders the request history page
@app.route('/requests_log', methods=['GET','POST'])
def get_Requests_data():
    data = db.session.query(Requests.id, Requests.username, Requests.text_request).order_by(Requests.id.desc()).limit(5)
    return render_template('requests_log.html',  data = data)

if __name__ == "__main__":
    app.run(debug=True)