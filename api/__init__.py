from flask import Flask
from flask_restx import Api
from .user.views import user_namespace
from .admin.views import admin_namespace
from .authentication.views import auth_namespace
from .config.config import config_dict


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    api = Api(app)

    api.add_namespace(user_namespace)
    api.add_namespace(admin_namespace, path='/admin')
    api.add_namespace(auth_namespace, path='/auth')

    return app
