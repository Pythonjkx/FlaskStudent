from flask import Flask
from flask import Blueprint

simple_blueprint = Blueprint('simple_page',__name__)


@simple_blueprint.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(simple_blueprint)#注册蓝图
    app.run()