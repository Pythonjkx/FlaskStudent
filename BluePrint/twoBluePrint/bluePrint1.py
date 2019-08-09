from flask import Blueprint

simple_bluePrint1 = Blueprint('simple_page1',__name__)

@simple_bluePrint1.route('/index1/')
def index():
    return 'hello world1'