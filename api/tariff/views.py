from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.tariff import Tariff
from http import HTTPStatus


tariff_namespace = Namespace('tariff', description="Standard tariff rates per kWh")

tariff_model = tariff_namespace.model(
    "Tariff", {
        "tariff_type": fields.String(required=True, description="Tariff type"),
        "value": fields.Float(required=True, description="Standard charges")
    }
)


@tariff_namespace.route('/')
class TariffRate(Resource):

    @tariff_namespace.marshal_with(tariff_model)
    def get(self):
        """
        Get all the tariff rates
        :return:
        """

        tariff_rates = Tariff.query.all()

        return tariff_rates, HTTPStatus.OK

    @tariff_namespace.expect(tariff_model)
    @tariff_namespace.marshal_with(tariff_model)
    def post(self):
        """
        Post a tariff rate
        :return:
        """
        tariff = request.get_json()

        new_tariff = Tariff(
            tariff_type=tariff.get('tariff_type'),
            value=tariff.get('value')
        )

        new_tariff.save()

        return new_tariff, HTTPStatus.CREATED

    def put(self):
        """
        Update a tariff rate
        :return:
        """
        pass
