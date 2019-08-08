import hashlib
from flask import render_template
from flask import redirect
from flask import request
from FlaskProject.main import app
from FlaskProject.models import *

def setPassword(password):
   md5 = hashlib.md5()
   md5.update(password.encode())
   return md5.hexdigest()


@app.route('/base/')
def hello_world():
    return render_template('base.html')



@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        from_data = request.form
        username = from_data.get('username')
        password = from_data.get('password')
        identity = from_data.get('identity')
        user = User()
        user.username = username
        user.password = setPassword(password)
        user.identity = int(identity)
        user.save()
        return redirect('/login/')
    return render_template('register.html')



@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        from_data = request.form
        username = from_data.get('username')
        password = from_data.get('password')
        if username and password:
            response = redirect('/index/')
            user = User.query.filter_by(username=username).first()
            if setPassword(password) == user.password:
                response.set_cookie('username',username)
                response.set_cookie('user_id',str(user.id))
                return response
    return render_template('login.html')

@app.route('/index/',methods=['GET','POST'])
def index():

    return render_template('index.html', **locals())

@app.route('/logOut/',methods=['GET','POST'])
def logOut():

    return render_template('stu.html', **locals())



@app.route('/stu/',methods=['GET','POST'])
def student_list():
    students = Student.query.all()
    return render_template('stu.html', **locals())


