from flask_cors import cross_origin
from flask_restx import Namespace, Resource, fields
from flask import request
from sqlalchemy import desc

from ..models.reading import Reading
from ..models.tariff import Tariff
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

reading_namespace = Namespace('reading', description="Meter Reading")

reading_model = reading_namespace.model(
    'Reading', {
        'readingId': fields.String(required=True, description="Id for the reading"),
        'customerId': fields.String(required=True, description="Customer Email Id"),
        'submissionDate': fields.DateTime(required=True, description="Reading submission date"),
        'elecReadingDay': fields.Float(required=True, description="Electricity Day Reading"),
        'elecReadingNight': fields.Float(required=True, description="Electricity Night Reading"),
        'gasReading': fields.Float(required=True, description="Gas Reading")
    }
)


@reading_namespace.route('/')
class MeterReading(Resource):

    @reading_namespace.marshal_with(reading_model)
    @jwt_required()
    def get(self):
        """
        Get all readings
        :return:
        """

        readings = Reading.query.all()

        return readings, HTTPStatus.OK

    @reading_namespace.expect(reading_model)
    @reading_namespace.marshal_with(reading_model)
    @jwt_required()
    def post(self):
        """
        Upload a meter reading
        :return:
        """
        data = request.get_json()
        readingdate = data.get('submissionDate')
        customer_id = get_jwt_identity()
        print(readingdate)

        new_reading = Reading(
            readingId=data.get('readingId'),
            customerId=customer_id,
            submissionDate=datetime.strptime(readingdate, '%Y-%m-%d').date(),
            elecReadingDay=data.get('elecReadingDay'),
            elecReadingNight=data.get('elecReadingNight'),
            gasReading=data.get('gasReading')
        )

        new_reading.save()

        return new_reading, HTTPStatus.CREATED


@reading_namespace.route('/getReadingById')
class GetReadingById(Resource):

    @reading_namespace.marshal_with(reading_model)
    @jwt_required()
    def get(self):
        """
        Get a meter reading by id
        :return:
        """

        user = get_jwt_identity()
        user_reading = Reading.get_reading_by_id(user)
        print(user_reading)

        return user_reading, HTTPStatus.OK


@reading_namespace.route('/getAllReadingById')
class GetAllReadingById(Resource):

    @reading_namespace.marshal_with(reading_model)
    @jwt_required()
    def get(self):
        """
        Get a meter reading by date
        :return:
        """
        user = get_jwt_identity()
        user_readings = Reading.query.order_by(desc(Reading.submissionDate)).filter_by(customerId=user).all()
        latest_reading = Reading.query.order_by(desc(Reading.submissionDate)).filter_by(customerId=user).limit(2).all()
        tariff_rate = Tariff.query.all()
        elec_day_tariff = Tariff.query.filter_by(tariff_type="Electricity Day").first()
        elec_night_tariff = Tariff.query.filter_by(tariff_type="Electricity Night").first()
        gas_tariff = Tariff.query.filter_by(tariff_type="Gas").first()
        standard_tariff = Tariff.query.filter_by(tariff_type="Standing Day Charge").first()
        print(latest_reading[0].submissionDate)
        current_reading = latest_reading[0]
        previous_reading = latest_reading[1]

        no_of_days = (current_reading.submissionDate-previous_reading.submissionDate).days
        print(no_of_days)
        elec_day_bill = (current_reading.elecReadingDay-previous_reading.elecReadingDay) * elec_day_tariff.value
        elec_night_bill = (current_reading.elecReadingNight-previous_reading.elecReadingNight) * elec_night_tariff.value
        gas_bill = (current_reading.gasReading-previous_reading.gasReading) * gas_tariff.value
        standard_bill = standard_tariff.value * no_of_days
        bill = elec_day_bill + elec_night_bill + gas_bill + standard_bill
        print(f"Bill, {round(bill,2)}")
        return user_readings

