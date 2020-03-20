from flask import Flask
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_executor import Executor
from config import Config
from ConsulClient import ConsulClient
from flask_apscheduler import APScheduler
users = {}

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in with your LDAP account to access this page'
ldap = LDAP3LoginManager()
bootstrap = Bootstrap()
consul_client = ConsulClient()
executor = Executor()
scheduler = APScheduler()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)
    ldap.init_app(app)
    bootstrap.init_app(app)
    consul_client.init_app(app)
    executor.init_app(app)

    from app.models import models

    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.main import bp as main_bp
    from app.blueprints.subnets import bp as subnets_bp
    from app.blueprints.exporters import bp as exporters_bp
    from app.blueprints.services import bp as services_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(subnets_bp, url_prefix='/subnets')
    app.register_blueprint(exporters_bp, url_prefix='/exporters')
    app.register_blueprint(services_bp, url_prefix='/services')


    return app
