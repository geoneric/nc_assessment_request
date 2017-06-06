from werkzeug.exceptions import *
from flask_restful import Resource
from flask import request
from .. import db
from .model import *
from .schema import *


assessment_request_schema = AssessmentRequestSchema()


class AssessmentRequestResource(Resource):


    def get(self,
            id):

        assessment_request = AssessmentRequestModel.query.get(id)

        if assessment_request is None:
            raise BadRequest("Assessment request could not be found")


        data, errors = assessment_request_schema.dump(assessment_request)

        if errors:
            raise InternalServerError(errors)


        return data


    def patch(self,
            id):

        json_data = request.get_json()

        if json_data is None:
            raise BadRequest("No input data provided")


        assessment_request = AssessmentRequestModel.query.get(id)

        if assessment_request is None:
            raise BadRequest("Assessment request could not be found")


        # Merge current representation and the edits passed in.
        for field_name in json_data:
            if hasattr(assessment_request, field_name):
                setattr(assessment_request, field_name, json_data[field_name])

        db.session.commit()


        data, errors = assessment_request_schema.dump(assessment_request)

        if errors:
            raise InternalServerError(errors)


        return data


    def delete(self,
            id):

        assessment_request = AssessmentRequestModel.query.get(id)

        if assessment_request is None:
            raise BadRequest("Assessment request could not be found")


        # Delete assessment_request from database.
        db.session.delete(assessment_request)
        db.session.commit()


        data, errors = assessment_request_schema.dump(assessment_request)

        if errors:
            raise InternalServerError(errors)


        return "", 204


class AssessmentRequestsResource(Resource):


    # TODO Only call this from admin interface!
    def get(self):

        assessment_requests = AssessmentRequestModel.query.all()
        data, errors = assessment_request_schema.dump(
            assessment_requests, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data


        return data


    def post(self):

        json_data = request.get_json()

        if json_data is None:
            raise BadRequest("No input data provided")


        # Validate and deserialize input.
        assessment_requests, errors = assessment_request_schema.load(json_data)

        if errors:
            raise UnprocessableEntity(errors)


        # Write assessment requests to database.
        db.session.add(assessment_requests)
        db.session.commit()


        # From record in database to dict representing an assessment request.
        data, errors = assessment_request_schema.dump(
            AssessmentRequestModel.query.get(assessment_requests.id))
        assert not errors, errors
        assert isinstance(data, dict), data


        return data, 201
