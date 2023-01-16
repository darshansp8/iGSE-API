from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.voucher import Voucher
from http import HTTPStatus
from ..utilities import db

voucher_namespace = Namespace('Voucher', description="Valid EVC")

voucher_model = voucher_namespace.model(
    'Voucher', {
        'evcCode': fields.String(required=True, description="Alphanumeric EVC code"),
        'used': fields.Boolean(required=True, description="Status of evc code")
    }
)


@voucher_namespace.route('/')
class Vouchers(Resource):

    @voucher_namespace.marshal_with(voucher_model)
    def get(self):
        """
        Get a evc
        :return:
        """

        voucher = Voucher.query.all()

        return voucher, HTTPStatus.OK

    @voucher_namespace.expect(voucher_model)
    @voucher_namespace.marshal_with(voucher_model)
    def post(self):
        """
        Add a evc
        :return:
        """
        data = request.get_json()

        new_voucher = Voucher(
            evcCode=data.get('evcCode'),
            used=data.get('used')
        )

        new_voucher.save()

        return new_voucher, HTTPStatus.CREATED

    @voucher_namespace.expect(voucher_model)
    @voucher_namespace.marshal_with(voucher_model)
    def put(self):

        data = voucher_namespace.payload
        voucher_to_update = Voucher.query.filter_by(evcCode=data['evcCode']).first()
        voucher_to_update.used = data['used']

        db.session.commit()

        return voucher_to_update


