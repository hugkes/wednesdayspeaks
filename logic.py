from main import *

# Defines the database table for history
class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=False, nullable=True)
    text_request = db.Column(db.String, unique=False, nullable=True)

# Logic for queue and thread 
class VoiceAssistant(Thread):
    def __init__(self):
        super(VoiceAssistant, self).__init__()
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.q = Queue()
        self.daemon = True

    def add_say(self, msg):
        self.q.put(msg)

    def run(self):
        while True:
            self.engine.say(self.q.get())
            try:
                self.engine.startLoop(False)
            except Exception as e:
                print ("Simultaneous request made")
            try:
                self.engine.iterate()
            except Exception as e:
                print ("Simultaneous request made")
            self.engine.endLoop()
            self.q.task_done()