from flask import Flask
from flask_admin import Admin
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_socketio import SocketIO


app = Flask(__name__)
# database settings
app.config['SECRET_KEY'] = 'secretTestKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tsbaza.db'
db = SQLAlchemy(app)

# SOCKETIO
socketio = SocketIO(app)

# LDAP Server and settings
app.config['LDAP_HOST'] = '<LDAP strežnik>'
app.config['LDAP_BASE_DN'] = '<LDAP base>'
app.config['LDAP_USER_DN'] = '<LDAP DN od uporabnikov>'
app.config['LDAP_GROUP_DN'] = '<LDAP skupina>'
app.config['LDAP_USER_RDN_ATTR'] = 'cn'
app.config['LDAP_USER_LOGIN_ATTR'] = 'cn'
app.config['LDAP_BIND_USER_DN'] = None
app.config['LDAP_BIND_USER_PASSWORD'] = None
app.config['LDAP_USE_SSL'] = True
app.config['LDAP_PORT'] = 636

# flask-admin settings
app.config['FLASK_ADMIN_SWATCH'] = 'Superhero'
admin = Admin(app, template_mode='bootstrap3')

# Setup a Flask-Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'

# Setup a LDAP3 Login Manager.
ldap_manager = LDAP3LoginManager(app)

# scheduler settings
class SchedConfig(object):
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///tsdashboard/tsbaza.db')
    }
    SCHEDULER_API_ENABLED = True

app.config.from_object(SchedConfig())
scheduler = APScheduler()
scheduler.init_app(app)
from tsdashboard.utile import app_scheduler
scheduler.start()


from tsdashboard import routes
from tsdashboard.apis.routes import apis
from tsdashboard.info.routes import info
from tsdashboard.main.routes import main
from tsdashboard.offenses.routes import offenses
from tsdashboard.statistika.routes import stats
from tsdashboard.users.routes import users
from tsdashboard.timers.routes import casi

app.register_blueprint(apis)
app.register_blueprint(info)
app.register_blueprint(main)
app.register_blueprint(offenses)
app.register_blueprint(stats)
app.register_blueprint(users)
app.register_blueprint(casi)
# app.register_blueprint(timers)



