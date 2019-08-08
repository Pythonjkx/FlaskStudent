import hashlib
from flask import render_template
from flask import redirect
from flask import request
from flask import jsonify
from FlaskProject.form import TeacherForm
from FlaskProject.main import app
from FlaskProject.models import *
from FlaskProject.main import session
from FlaskProject.main import csrf

def setPassword(password):
   md5 = hashlib.md5()
   md5.update(password.encode())
   return md5.hexdigest()


@app.route('/base/')
def hello_world():
    return render_template('base.html')

def loginVaild(fun):
    def inner(*args,**kwargs):
        user_cookie = request.cookies.get('username')
        id = request.cookies.get('user_id')
        user_session = session.get('username')
        if user_cookie and id and user_session:
            if user_cookie == user_session:
                return fun(*args,**kwargs)
        return redirect('/login/')
    return inner

@csrf.exempt
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


@csrf.exempt
@app.route('/login/',methods=['GET','POST'])
def login():
    result = {'message':''}
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
                session['username'] = username
                return response
            else:
                result['message'] = '用户名或密码错误'
        else:
            result['message'] = '用户名或密码不能为空'
    return render_template('login.html',**locals())

@csrf.exempt
@app.route('/index/',methods=['GET','POST'])
@loginVaild
def index():
    return render_template('index.html', **locals())


@app.route('/logOut/',methods=['GET','POST'])
def logOut():
    response = redirect('/login/')
    cookie_list = request.cookies
    for key in cookie_list:
        response.delete_cookie(key)
    del session['username']
    return response



@app.route('/stu/',methods=['GET','POST'])
def student_list():
    students = Student.query.all()
    return render_template('stu.html', **locals())


@csrf.exempt
@app.route('/teachers/',methods=['GET','POST'])
def add_teacher():
    teacher = TeacherForm()
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        course = request.form.get('course')

        t = Teacher()
        t.name = name
        t.age = age
        t.gender = gender
        t.course_id = int(course)
        t.save()
    return render_template('add_teacher.html',**locals())


# @csrf.error_handler
@app.route('/csrf_403/')
def csrf_token_error():
    # print(reason)
    return render_template('csrf_403.html')


@csrf.exempt
@app.route('/userValid/',methods=['POST','GET'])
def userValid():
    result = {'code':'','data':''}
    if request.method == 'POST':
        user = request.form.get('username')
        if user:
            username = User.query.filter_by(username = user).first()
            if username:
                result['code'] = 400
                result['data'] = '用户名已存在'
            else:
                result['code'] = 200
                result['data'] = '用户名可以使用'
        else:
            result['code'] = 400
            result['data'] = '用户名不可以为空'
    else:
        result['data'] = '提交方式有误'
        result['code'] = 400
    return jsonify(result)

