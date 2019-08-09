from flask import Flask
from flask_script import Manager

app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world'

manage = Manager(app)#对app进行序列化

if __name__ == '__main__':
    manage.run()