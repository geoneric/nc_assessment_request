import json
import os.path
import traceback
from werkzeug.exceptions import *
from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_from_directory
from .. import db, uploaded_results
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
        assessment_request, errors = assessment_request_schema.load(json_data)

        if errors:
            raise UnprocessableEntity(errors)


        # Write assessment request to database.
        db.session.add(assessment_request)
        db.session.commit()


        # From record in database to dict representing an assessment request.
        data, errors = assessment_request_schema.dump(
            AssessmentRequestModel.query.get(assessment_request.id))
        assert not errors, errors
        assert isinstance(data, dict), data


        return data, 201


assessment_result_schema = AssessmentResultSchema()


class AllAssessmentResultsResource(Resource):


    def get(self):

        results = AssessmentResultModel.query.all()
        data, errors = assessment_result_schema.dump(results, many=True)

        if errors:
            raise InternalServerError(errors)

        return data


    def post(self):

        # The data passed in should contain a zip file and a JSON snippet
        # with some additional information
        # We must do the folowing:
        # - Grab the request id which this result is related to
        # - Save the file
        # - Store metadata

        try:
            data = json.loads(request.form["data"])

            # request.files["result"] -> FileStorage
            # request.files["result"].name -> result
            # request.files["result"].filename -> result.zip
            filename = uploaded_results.save(
                request.files["result"], folder=data["request_id"])
            pathname = uploaded_results.path(filename)

        except UploadNotAllowed:
            raise BadRequest("uploading {} not allowed".format(
                request.files["result"]))
        except Exception as exception:
            raise BadRequest(
                "invalid upload request, exception: {}, form: {}, "
                "files: {}".format(traceback.format_exc(), request.form,
                    request.files))

        json_data = {
            "assessment_result": {
                "request_id": data["request_id"],
                "data": pathname,
            }
        }


        # Validate and deserialize input.
        resource, errors = assessment_result_schema.load(json_data)

        if errors:
            raise UnprocessableEntity(errors)


        # Write resource to database.
        db.session.add(resource)
        db.session.commit()


        # From record in database to dict representing an assessment result.
        data, errors = assessment_result_schema.dump(
            AssessmentResultModel.query.get(resource.id))
        assert not errors, errors
        assert isinstance(data, dict), data


        return data, 201


class GroupedAssessmentResultsResource(Resource):


    def get(self,
            request_id):

        resources = AssessmentResultModel.query.filter_by(
            request_id=request_id)
        data, errors = assessment_result_schema.dump(resources, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data

        return data


class AssessmentResultResource(Resource):


    def get(self,
            request_id,
            id):

        # request_id is not needed
        resource = AssessmentResultModel.query.get(id)

        if resource is None or resource.request_id != request_id:
            raise BadRequest("Assessment result could not be found")

        data, errors = assessment_result_schema.dump(resource)

        if errors:
            raise InternalServerError(errors)

        return data


    def delete(self,
            request_id,
            id):

        # request_id is not needed
        resource = AssessmentResultModel.query.get(id)

        if resource is None or resource.request_id != request_id:
            raise BadRequest("Assessment result could not be found")


        # Delete resource from database.
        db.session.delete(resource)
        db.session.commit()


        data, errors = assessment_result_schema.dump(resource)

        if errors:
            raise InternalServerError(errors)


        return "", 204


class AssessmentResultData(Resource):


    def get(self,
            request_id,
            id):

        # Retrieve the result resource with the given id
        resource = AssessmentResultModel.query.get(id)

        if resource is None or resource.request_id != request_id:
            raise BadRequest("Assessment result could not be found")

        print(resource)
        print(dir(resource))
        pathname = resource.data

        return send_from_directory(
            *os.path.split(pathname), as_attachment=True)


assessment_indicator_result_schema = AssessmentIndicatorResultSchema()


class AllAssessmentIndicatorResultsResource(Resource):


    def get(self):

        results = AssessmentIndicatorResultModel.query.all()
        data, errors = assessment_indicator_result_schema.dump(
            results, many=True)

        if errors:
            raise InternalServerError(errors)


        return data


    def post(self):

        json_data = request.get_json()

        if json_data is None:
            raise BadRequest("No input data provided")


        # Validate and deserialize input.
        resource, errors = assessment_indicator_result_schema.load(json_data)

        if errors:
            raise UnprocessableEntity(errors)


        # Write resource to database.
        db.session.add(resource)
        db.session.commit()


        # From record in database to dict representing an assessment result.
        data, errors = assessment_indicator_result_schema.dump(
            AssessmentIndicatorResultModel.query.get(resource.id))
        assert not errors, errors
        assert isinstance(data, dict), data


        return data, 201


class GroupedAssessmentIndicatorResultsResource(Resource):


    def get(self,
            result_id):

        resources = AssessmentIndicatorResultModel.query.filter_by(
            result_id=result_id)
        data, errors = assessment_indicator_result_schema.dump(
            resources, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data


        return data


class AssessmentIndicatorResultResource(Resource):


    def get(self,
            result_id,
            id):

        # result_id is not needed
        assessment_indicator_result = \
            AssessmentIndicatorResultModel.query.get(id)

        if assessment_indicator_result is None or \
                assessment_indicator_result.result_id != result_id:
            raise BadRequest("Assessment indicator result could not be found")


        data, errors = assessment_indicator_result_schema.dump(
            assessment_indicator_result)

        if errors:
            raise InternalServerError(errors)


        return data


    def delete(self,
            result_id,
            id):

        # result_id is not needed
        resource = \
            AssessmentIndicatorResultModel.query.get(id)

        if resource is None or resource.result_id != result_id:
            raise BadRequest("Assessment indicator result could not be found")


        # Delete resource from database.
        db.session.delete(resource)
        db.session.commit()


        data, errors = assessment_indicator_result_schema.dump(resource)

        if errors:
            raise InternalServerError(errors)


        return "", 204
