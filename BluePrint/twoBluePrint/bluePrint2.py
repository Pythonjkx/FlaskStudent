from flask import Blueprint

simple_bluePrint2 = Blueprint('simple_page2',__name__)

@simple_bluePrint2.route('/index2/')
def index():
    return 'hello world2'