from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from ..models.customer import Customer
from ..models.voucher import Voucher
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token

auth_namespace = Namespace('auth', description="Authenticating the users")

signup_model = auth_namespace.model(
    'SignUp', {
        'customer_id': fields.String(required=True, description="Email id is used as a customer id"),
        'password': fields.String(required=True, description="A password"),
        'propertyType': fields.String(reequired=True, description="A property type"),
        'bedroomNum': fields.Integer(required=True, description="Number of Bedrooms"),
        'address': fields.String(required=True, description="Home Address"),
        'balance': fields.Float(required=True, description="Customer Balance"),
        'type': fields.String(description="User role customer/admin")
    }
)

customer_model = auth_namespace.model(
    "Customer", {
        'customer_id': fields.String(required=True, description="Email id is used as a customer id"),
        'password_hash': fields.String(required=True, description="A password"),
        'propertyType': fields.String(reequired=True, description="A property type"),
        'bedroomNum': fields.Integer(required=True, description="Number of Bedrooms"),
        'address': fields.String(required=True, description="Home Address"),
        'balance': fields.Float(required=True, description="Customer Balance"),
        'type': fields.String(description="User role customer/admin")
    }
)

response_model = auth_namespace.model(
    "Response", {
        'access_token': fields.String(required=True),
        'customer_id': fields.String(required=True, description="Email id is used as a customer id"),
        'password_hash': fields.String(required=True, description="A password"),
        'propertyType': fields.String(reequired=True, description="A property type"),
        'bedroomNum': fields.Integer(required=True, description="Number of Bedrooms"),
        'address': fields.String(required=True, description="Home Address"),
        'balance': fields.Float(required=True, description="Customer Balance"),
        'type': fields.String(description="User role customer/admin")
    }
)

login_model = auth_namespace.model(
    "Login", {
        'customer_id': fields.String(required=True, description="Email id is used for login"),
        'password': fields.String(required=True, description="A password")
    }
)


@auth_namespace.route('/signup')
class SignUp(Resource):

    @auth_namespace.expect(signup_model)
    # @auth_namespace.marshal_with(response_model)
    def post(self):
        """
        Create a new user
        """
        data = request.get_json()
        balance = 200
        type = "user"

        new_user = Customer(
            customer_id=data.get('customer_id'),
            password_hash=generate_password_hash(data.get('password')),
            propertyType=data.get('propertyType'),
            bedroomNum=data.get('bedroomNum'),
            address=data.get('address'),
            balance=balance,
            type=type
        )

        is_user = Customer.query.filter_by(customer_id=new_user.customer_id).first()

        voucher = Voucher.query.filter_by(evcCode=data.get('evcCode')).first()
        print(voucher)

        if voucher is not None:

            if (is_user is None) and (voucher.used is False):
                print("Inside If")
                access_token = create_access_token(identity=new_user.customer_id)
                refresh_token = create_refresh_token(identity=new_user.customer_id)

                new_user.save()

                response = {
                    'data': {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'httpstatus': HTTPStatus.CREATED,
                        'type': new_user.type,
                        'customerId': new_user.customer_id
                    },
                    'errorMessage': ''
                }

                return response, HTTPStatus.CREATED

            elif is_user is not None:
                print("Inside else")
                response = {
                    'data': '',
                    'errorMessage': {
                        'message': 'Customer Id already exists',
                        'errorCode': 0
                    }
                }
                return response, HTTPStatus.INTERNAL_SERVER_ERROR

            elif voucher.used:
                response = {
                    'data': '',
                    'errorMessage': {
                        'message': 'Voucher is already used!',
                        'errorCode': 1
                    }
                }

                return response, HTTPStatus.INTERNAL_SERVER_ERROR

        else:
            print("Inside else: Invalid Voucher")
            response = {
                'data': '',
                'errorMessage': {
                    'message': 'Invalid',
                    'errorCode': 2
                }
            }

            return response, HTTPStatus.INTERNAL_SERVER_ERROR


@auth_namespace.route('/login')
class Login(Resource):

    @auth_namespace.expect(login_model)
    def post(self):
        """
        Login existing user / Generate a JWT
        :return:
        """

        data = request.get_json()

        customer_id = data.get('customer_id')
        password = data.get('password')

        user = Customer.query.filter_by(customer_id=customer_id).first()
        # print(user.password_hash)

        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.customer_id)
            refresh_token = create_refresh_token(identity=user.customer_id)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            # resp = json.dumps(response)

            return response, HTTPStatus.OK

        else:
            return "Invalid input"
