from app import models


class BaseModel(models.Model):
    __abstract__ = True
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)

    def save(self):
        db.add(self)
        db.commit()

    def delete_obj(self):
        db.delete(self)
        db.commit()

class User(BaseModel):
    __tablename__ = 'user'
    username = models.Column(models.String(32))
    password = models.Column(models.String(32))
    identity = models.Column(models.Integer)#0 教师 1 学生
    identity_id = models.Column(models.Integer,default='',nullable=True)

# 学员表
class Student(BaseModel):
    __tablename__ = 'student'
    name = models.Column(models.String(32),unique=True)
    age = models.Column(models.Integer)
    gender = models.Column(models.Integer)#0 男 1 女 -1 中

# 成绩表
class Grade(BaseModel):
    __tablename__ = 'grade'
    grade = models.Column(models.Float,default=0)
    course_id = models.Column(models.Integer, models.ForeignKey('course.id'))
    student_id = models.Column(models.Integer, models.ForeignKey('student.id'))

# 教师表
class Teacher(BaseModel):
    __tablename__ = 'teacher'
    name = models.Column(models.String(32))
    age = models.Column(models.Integer)
    gender = models.Column(models.Integer,default=3)#0 男 1 女 -1 中
    course_id = models.Column(models.Integer, models.ForeignKey('course.id'))


Stu_Cou = models.Table(
    'stu_cou',
    models.Column('id',models.Integer, primary_key=True, autoincrement=True),
    models.Column('course_id',models.Integer,models.ForeignKey('course.id')),
    models.Column('student_id',models.Integer,models.ForeignKey('student.id')),
)

# 课程表
class Course(BaseModel):
    __tablename__ = 'course'
    lable = models.Column(models.String(32))
    description = models.Column(models.Text)

    to_teacher = models.relationship(
        'Teacher',
        backref = 'to_course1'
    )

    to_student = models.relationship(
        'Student',
        secondary = Stu_Cou,
        backref = models.backref('to_course',lazy = 'dynamic'),
        lazy = 'dynamic'
    )






# 考勤表
class Kaoqin(BaseModel):
    __tablename__ = 'kaoqin'
    kao_time = models.Column(models.Date)
    status = models.Column(models.Integer,default=1)#0 迟到 1 正常 2 早退 3 请假 4 旷课
    student_id = models.Column(models.Integer, models.ForeignKey('student.id'))

# models.create_all()

# 学员、课程表
# class Stu_Cou(BaseModel):
#     __tablename__ = 'stu_cou'
#     course_id = models.Column(models.Integer,models.ForeignKey('course.id'))
#     student_id = models.Column(models.Integer,models.ForeignKey('student.id'))


# models.drop_all()
# models.create_all()
# course = Course(lable='python',description='lll')
# course.save()
# course1 = Course(lable='ui',description='hao')
# course1.save()
# course2 = Course(lable='java',description='oo')
# course2.save()
# stu = Student(name='xioali',age=18,gender='男')
# stu.save()
# stu1 = Student(name='lo',age=20,gender='女')
# stu1.save()
# stu.to_course = [course]
# stu.save()
# stu1.to_course = [course1,course2]
# stu1.save()
# course2 = Course()
# course2.lable = 'java'
# course2.description = '不行啊'
# course3 = {'lable':'UI','description':'好多美女'}
# course4 = Course(**course3)
# session.add_all([course2,course4])
# session.commit()
# Teacher(name='老陈',age=25,gender='男',course_id=2).save()
# t = Teacher.query.get(1).delete_obj()

# teachers = Teacher.query.all()
# teacher = Teacher.query.filter_by(age = 18).all()
# teacher = Teacher.query.get(4)
# teacher = Teacher.query.order_by(Teacher.age.desc()).all()
# print(teacher)
# teacher = Teacher.query.get(3)
# teacher.name = '老李'
# models.session.commit()
# teacher = Teacher.query.offset(0).limit(2).all()
# print(teacher)
# teacher = Teacher.query.group_by('age').all()
# print(teacher)
# c = Course.query.get(1)
# print(c.to_teacher)
# t = Teacher.query.get(1)
# print(t.to_course1)