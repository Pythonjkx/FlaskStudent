from flask import Flask
from flask_script import Manager
from bluePrint1 import simple_bluePrint1
from bluePrint2 import simple_bluePrint2

app = Flask(__name__)
app.register_blueprint(simple_bluePrint1)
app.register_blueprint(simple_bluePrint2)
manage = Manager(app)
if __name__ == '__main__':

    manage.run()