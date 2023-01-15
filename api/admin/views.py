from flask_restx import Namespace, Resource

admin_namespace = Namespace('admin', description="Authenticating the users")


@admin_namespace.route('/')
class HelloAdmin(Resource):

    def get(self):
        return {'message': "Hello Admin"}


@admin_namespace.route('/updateTariff')
class UpdateTariff(Resource):

    def put(self):
        """
        Update Tariff
        """
        pass
