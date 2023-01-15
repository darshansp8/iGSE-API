from flask_restx import Namespace, Resource

from ..models.voucher import Voucher
from ..authentication.views import signup_model
from ..models.customer import Customer
from http import HTTPStatus
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utilities import db

user_namespace = Namespace('users', description="User route")

user_model = signup_model


@user_namespace.route('/')
class GetAllUsers(Resource):

    @user_namespace.marshal_with(user_model)
    def get(self):
        """
        Get all users
        """

        users = Customer.query.all()

        return users, HTTPStatus.OK


@user_namespace.route('/getUserById')
class GetUserById(Resource):

    @user_namespace.marshal_with(user_model)
    @jwt_required()
    def get(self):
        """
        Get a user by Id
        :return:
        """
        user = get_jwt_identity()
        single_customer = Customer.get_user_by_id(user)

        return single_customer, HTTPStatus.OK


@user_namespace.route("/deleteUserById")
class DeleteUserById(Resource):

    @user_namespace.marshal_with(user_model)
    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        user_to_delete = Customer.get_user_by_id(user_id)
        user_to_delete.delete()

        return user_to_delete


@user_namespace.route("/updatebalance")
class UpdateWallet(Resource):

    @user_namespace.expect(user_model)
    @user_namespace.marshal_with(user_model)
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        print(f"Hello, {user_id}")
        user_to_update = Customer.query.filter_by(customer_id=user_id).first()
        data = user_namespace.payload
        print(user_to_update.balance)
        voucher = Voucher.query.filter_by(evcCode=data['evcCode']).first()

        if voucher is not None and voucher.used is False:
            current_balance = user_to_update.balance
            new_balance = current_balance + 200
            user_to_update.balance = new_balance
            voucher.used = True
            db.session.commit()

            return user_to_update

