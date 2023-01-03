from flask_restx import Namespace, Resource

admin_namespace = Namespace('admin', description="Authenticating the users")


@admin_namespace.route('/')
class HelloAdmin(Resource):

    def get(self):
        return {'message': "Hello Admin"}
