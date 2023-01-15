from flask import Flask
from flask_restx import Api
from .user.views import user_namespace
from .admin.views import admin_namespace
from .authentication.views import auth_namespace
from .tariff.views import tariff_namespace
from .readings.views import reading_namespace
from .voucher.views import voucher_namespace
from .config.config import config_dict
from .utilities import db
from .models.customer import Customer
from .models.reading import Reading
from .models.tariff import Tariff
from .models.voucher import Voucher
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    CORS(app, resources={r"*": {'origins': '*', 'methods': ['OPTIONS', 'GET', 'POST', 'DELETE', 'PUT']}})

    app.config.from_object(config)

    # Database connection
    db.init_app(app)
    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    api = Api(app)

    api.add_namespace(user_namespace)
    api.add_namespace(admin_namespace, path='/admin')
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(tariff_namespace, path="/tariff")
    api.add_namespace(reading_namespace, path="/readings")
    api.add_namespace(voucher_namespace, path="/voucher")

    @app.shell_context_processor
    def make_shell_context():
        return{
            'db': db,
            'Customer': Customer,
            'Reading': Reading,
            'Tariff': Tariff,
            'Voucher': Voucher
        }

    return app
