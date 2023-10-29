from flask import Flask
import hashlib, os
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect

# csrf = CSRFProtect()
app = Flask(__name__)
# csrf.init_app(app)


SALT_BITS = 32
HASH_MODE = 'sha256'
ITERATION = 10000
HASH_MODE_TOKEN = 'HS256'
app.secret_key = 'the random string'

from app import global_view
from app.views.auth.view import auth
from app.views.profile.view import profile
from app.views.admin.view import admin
from app.views.report.view import report
from app.views.request.view import request
from app.views.help.view import help_page
# from flask_login import LoginManager



app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(admin)
app.register_blueprint(report)
app.register_blueprint(request)
app.register_blueprint(help_page)
# login = LoginManager(app) #new line


moment = Moment(app)

