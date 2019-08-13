from app import create_app,models
from flask_script import Manager
from flask_migrate import Migrate #用来同步数据库
from flask_migrate import MigrateCommand #用来同步数据库的命令
from gevent import monkey #猴子补丁

monkey.patch_all()#猴子补丁，将之前代码当中所有不契合协程的代码修改为契合


app = create_app('running') #实例化app

manage = Manager(app) #命令行封装

migrate = Migrate(app,models) #绑定可以管理的数据库模型

manage.add_command('db',MigrateCommand) #加载数据库管理命令

@manage.command
def runserver_gevent():
    from gevent import pywsgi
    server = pywsgi.WSGIServer(('127.0.0.1',5000),app)
    server.serve_forever()

if __name__ == '__main__':
    manage.run()
