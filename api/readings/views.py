from flask_cors import cross_origin
from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.reading import Reading
from http import HTTPStatus
from flask_jwt_extended import jwt_required

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

        new_reading = Reading(
            readingId=data.get('readingId'),
            customerId=data.get('customerId'),
            submissionDate=data.get('submissionDate'),
            elecReadingDay=data.get('elecReadingDay'),
            elecReadingNight=data.get('elecReadingNight'),
            gasReading=data.get('gasReading')
        )

        new_reading.save()

        return new_reading, HTTPStatus.CREATED


@reading_namespace.route('/getReadingById')
class GetReadingById(Resource):

    def get(self, id):
        """
        Get a meter reading by id
        :return:
        """
        pass


@reading_namespace.route('/getReadingByDate')
class GetReadingByDate(Resource):

    def get(self, date):
        """
        Get a meter reading by date
        :param date:
        :return:
        """
        pass