import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'jkx123' #用来生成session_id和csrf_token
    CACHE_TYPE = 'simple'
class DebugConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:0000@localhost/students'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'Student.sqlite')

class OnlineConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'Student.sqlite')