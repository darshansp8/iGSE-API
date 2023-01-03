from flask_restx import Namespace, Resource

user_namespace = Namespace('users', description="User route")


@user_namespace.route('/')
class HelloUser(Resource):

    def get(self):
        return {'message': "Hello User"}
