import os

from dotenv import load_dotenv
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

application = Flask(__name__)
application.wsgi_app = ProxyFix(application.wsgi_app, x_for=1, x_proto=1, x_host=1)
application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')
DBVAR = f"postgresql://{os.environ['RDS_USERNAME']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOSTNAME']}/{os.environ['RDS_DB_NAME']}?sslmode=require"
application.config['SQLALCHEMY_DATABASE_URI'] = DBVAR
application.config['SQLALCHEMY_BINDS'] = {'transport': DBVAR}
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(application)
db = SQLAlchemy(application)
login_manager = LoginManager(application)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from capp.carbon_app.routes import carbon_app  # noqa: E402
from capp.home.routes import home  # noqa: E402
from capp.methodology.routes import methodology  # noqa: E402
from capp.users.routes import users  # noqa: E402

application.register_blueprint(home)
application.register_blueprint(methodology)
application.register_blueprint(carbon_app)
application.register_blueprint(users)

with application.app_context():
    db.create_all()
