import wtforms #定义字段
from flask_wtf import Form #定义表单的父类
from wtforms import validators #定义校验
# from app.models import Course
# course_list = [(c.id,c.lable) for c in Course.query.all()]
course_list = []
class TeacherForm(Form):
    name = wtforms.StringField('教师姓名',
                               render_kw={
                                   'class':'form-control',
                                   'placeholder':'教师姓名'
                               },
                               validators=[
                                   validators.DataRequired('姓名不可为空')
                               ]
                               )
    age = wtforms.StringField('教师年龄',
                               render_kw={
                                   'class': 'form-control',
                                   'placeholder': '教师年龄'
                               },
                               validators=[
                                   validators.DataRequired('年龄不可为空')
                               ]
                               )
    gender = wtforms.SelectField(
        '教师性别',
        choices=[
            ('1','男'),
            ('2','女')
        ]
        ,
        render_kw={
            'class':'form-control',
        }
    )
    course = wtforms.SelectField(
        '学科',
        choices=course_list
        ,
        render_kw={
            'class':'form-control',
        }
    )