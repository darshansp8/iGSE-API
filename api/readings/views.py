from flask_cors import cross_origin
from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.reading import Reading
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



# @reading_namespace.route('/getReadingByDate')
class GetReadingByDate(Resource):

    def get(self, date):
        """
        Get a meter reading by date
        :param date:
        :return:
        """
        pass