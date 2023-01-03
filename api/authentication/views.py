from flask_restx import Namespace, Resource

auth_namespace = Namespace('auth', description="Authenticating the users")


@auth_namespace.route('/')
class HelloAuth(Resource):

    def get(self):
        return {'message': "Hello Auth"}
