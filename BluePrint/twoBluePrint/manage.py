from flask import Flask
from twoBluePrint.bluePrint1 import *
from twoBluePrint.bluePrint2 import *


if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(simple_bluePrint1)
    app.register_blueprint(simple_bluePrint2)
    app.run()