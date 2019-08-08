from FlaskProject.models import models
from FlaskProject.views import app

if __name__ == '__main__':
    # models.create_all()
    app.run(use_reloader = False)