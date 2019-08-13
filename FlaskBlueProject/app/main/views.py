import hashlib
from flask import render_template
from flask import redirect
from flask import request
from flask import jsonify
from flask import make_response

from . import main
from flask import session
from app import csrf
from app import cache
from app.models import *
from .forms import TeacherForm

def setPassword(password):
   md5 = hashlib.md5()
   md5.update(password.encode())
   return md5.hexdigest()


@main.route('/base/')
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
@main.route('/register/',methods=['GET','POST'])
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
@main.route('/login/',methods=['GET','POST'])

def login():
    result = {'message':''}
    if request.method == 'POST':
        from_data = request.form
        username = from_data.get('username')
        password = from_data.get('password')
        if username and password:
            response = redirect('/index/')
            user = User.query.filter_by(username=username).first()
            identity = user.identity
            identity_id = user.identity_id
            if setPassword(password) == user.password:
                identity =  user.identity
                response.set_cookie('username',username)
                response.set_cookie('user_id',str(user.id))
                session['username'] = username
                response.set_cookie('identity',str(identity))#下发身份cookies
                if identity_id:
                    response.set_cookie('identity_id',str(identity_id))
                else:
                    response.set_cookie('identity_id','')
                return response
            else:
                result['message'] = '用户名或密码错误'
        else:
            result['message'] = '用户名或密码不能为空'
    return render_template('login.html',**locals())

@csrf.exempt
@main.route('/index/',methods=['GET','POST'])
@loginVaild
# @cache.cached(timeout=50)
def index():
    c = Course.query.all()
    username = request.cookies.get('username')
    user = User.query.filter_by(username = username).first()
    if user.identity == 1: #断是否为学生
        s = Student()
        s.name = username
        s.age = request.form.get('age')
        s.gender = request.form.get('gender')
        s.save()
    else:
        username = request.cookies.get('username')
        id  = request.cookies.get('user_id')
        user = User.query.filter_by(username=username).first()#第一对象的实例

        if user.identity_id:#判断是否完善信息
            teacher = Teacher.query.filter_by(id=int(user.identity_id)).first()#找老师表
            course = teacher.to_course1
        else:
            if request.method == "POST":
                t = Teacher()
                t.name = username
                t.age = request.form.get('age')
                t.gender = request.form.get('gender')
                t.course_id = request.form.get('course_id')
                t.save()
                # 更新用户和教师关联
                user.identity_id = t.id
                user.save()
                course = t.to_course1 #反向查询出教师对应的课程
                response = make_response(render_template('index.html', **locals()))
                response.set_cookie('identity_id', str(t.id))
                return response
    return render_template('index.html',**locals())


@main.route('/logOut/',methods=['GET','POST'])
def logOut():
    response = redirect('/login/')
    cookie_list = request.cookies
    for key in cookie_list:
        response.delete_cookie(key)
    del session['username']
    return response



@main.route('/stu/',methods=['GET','POST'])
def student_list():
    students = Student.query.all()
    return render_template('stu.html', **locals())


@csrf.exempt
@main.route('/add_teachers/',methods=['GET','POST'])
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
@main.route('/csrf_403/')
def csrf_token_error():
    # print(reason)
    return render_template('csrf_403.html')


@csrf.exempt
@main.route('/userValid/',methods=['POST','GET'])
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


# 学生个人信息
@csrf.exempt
@main.route('/student/',methods=['POST','GET'])
def student():
    name = request.cookies.get('username')
    id = request.cookies.get('user_id')#获取用户id
    user = User.query.get(int(id))
    student = Student.query.get(int(user.identity_id))
    course = student.to_course
    print(course)
    return render_template('student.html',**locals())



# 学生列表
@csrf.exempt
@main.route('/students/',methods=['POST','GET'])
def students_list():
    student = Student.query.all()
    return render_template('students.html',**locals())

#删除学生
@csrf.exempt
@main.route('/del_student/',methods=['POST','GET'])
def del_student():
    id = request.args.get('student_id')
    student = Student.query.filter_by(id = id).first()
    student.delete_obj()
    return redirect('/students/')


# 教师个人信息
@csrf.exempt
@main.route('/teacher/',methods=['POST','GET'])
def teacher():
    name = request.cookies.get('username')
    teacher = Teacher.query.filter_by(name=name).first()
    course = teacher.to_course1 #反向查询
    return render_template('teacher.html',**locals())


# 教师列表
@csrf.exempt
@main.route('/teachers/',methods=['POST','GET'])
def teachers_list():
    teacher = Teacher.query.all()
    course = Course.query.all()
    return render_template('teachers.html',**locals())

#删除老师
@csrf.exempt
@main.route('/del_teacher/',methods=['POST','GET'])
def del_teacher():
    id = request.args.get('teacher_id')
    teahcer = Teacher.query.filter_by(id = id).first()
    teahcer.delete_obj()
    return redirect('/teachers/')

# 所有课程
@csrf.exempt
@main.route('/all_course/',methods=['POST','GET'])
def all_course():
    course = Course.query.all()
    if request.method == 'POST':
        lable = request.form.get('name')
        description = request.form.get('description')
        if lable and description:
            coures = Course()
            coures.lable = lable
            coures.description = description
            coures.save()
    return render_template('all_course.html',**locals())

# 修改课程
@csrf.exempt
@main.route('/update_course/',methods=['POST','GET'])
def update_course():
    course_id = request.args.get('course_id')
    coueses = Course.query.filter_by(id=int(course_id)).first()
    if request.method == 'POST':
        lable = request.form.get('name')
        description = request.form.get('description')
        if lable and description:
            coueses.lable = lable
            coueses.description = description
            coueses.save()
            return redirect('/all_course/')
    return render_template('update_course.html',**locals())

# 删除课程
@csrf.exempt
@main.route('/del_course/',methods=['POST','GET'])
def del_course():
    id = request.args.get('course_id')
    course = Course.query.filter_by(id = id).first()
    course.delete_obj()
    return redirect('/all_course/')



#摸版视图
@csrf.exempt
@main.route('/base/',methods=['POST','GET'])
def base():
    return render_template('base.html')

# 清理缓存
@main.route('/clearCache/')
def claerCache():
    cache.clear()
    return 'is over'