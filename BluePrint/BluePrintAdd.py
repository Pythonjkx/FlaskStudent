from flask import Flask
from flask_script import Manager

app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world'

manage = Manager(app)#对app进行序列化
@manage.command
def hello(name='createsuperuser'):
    username = input('请输入用户名：')
    password = input('请输入用密码：')
    email = input('请输入用邮箱：')
    print('执行成功%s'%name)
    return 'yes'

@manage.command
def runs(ip='127.0.0.1',port=8000):
    print('runserver in %s:%s'%(ip,port))


if __name__ == '__main__':
    manage.run()

