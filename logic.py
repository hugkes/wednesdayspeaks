from main import *

# Defines the database Requests for history
class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=False, nullable=True)
    text_request = db.Column(db.String, unique=False, nullable=True)
    said_flag = db.Column(db.Boolean, unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)


# Setup of database (note subsequent runs of this wont re-create)
#db.create_all()

# Logic for queue and thread
class VoiceAssistant():
    def __init__(self):
        pythoncom.CoInitialize()

    def say(self, text):
        if "hate" in text:
            text = "I hate Anna"
        text = "um " + text
        speaker = wincl.Dispatch("SAPI.SpVoice")
        speaker.Speak(text)

class HandleRequest():
    def __init__(self):
        #Kicks off logic when request made, renders message
        pass

    def add_db_msg(self, user, text):
        message = ''
        now = datetime.now()
        if len(text) < 250 and len(text.split()) < 40:
            db.session.add(Requests(username=user, text_request = text, said_flag = False, timestamp = now))
            db.session.commit()
            message = "thanks bbg"
        else:
            message = "Requested speech is too long. Please shorten your message."
        return message