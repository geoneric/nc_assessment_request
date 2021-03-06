import datetime
import uuid
from marshmallow import fields, post_dump, post_load, pre_load, ValidationError
from marshmallow.validate import Length, OneOf
from .. import ma
from .model import *


class AssessmentRequestSchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = ("id", "plan", "status", "posted_at", "patched_at", "_links")

    id = fields.UUID(dump_only=True)
    plan = fields.Str(required=True, validate=Length(min=1))
    status = fields.Str(dump_only=True,
        validate=OneOf(["pending", "queued", "executing", "failed",
            "succeeded"]))
    posted_at = fields.DateTime(dump_only=True)
    patched_at = fields.DateTime(dump_only=True)
    _links = ma.Hyperlinks({
        "self": ma.URLFor("api.assessment_request", id="<id>"),
        "collection": ma.URLFor("api.assessment_requests")
    })


    def key(self,
            many):
        return "assessment_requests" if many else "assessment_request"


    @pre_load(
        pass_many=True)
    def unwrap(self,
            data,
            many):
        key = self.key(many)

        if key not in data:
            raise ValidationError("Input data must have a {} key".format(key))

        return data[key]


    def wrap_links(self,
            request):

        # Insert links that are useful, given the state of the request.
        if request["status"] == "succeeded":
            request["_links"]["result"] = \
                "/assessment_results/{}".format(request["id"])


    @post_dump(
        pass_many=True)
    def wrap(self,
            data,
            many):

        if not many:
            self.wrap_links(data)
        else:
            for request in data:
                self.wrap_links(request)

        key = self.key(many)

        return {
            key: data
        }


    @post_load
    def make_object(self,
            data):
        return AssessmentRequestModel(
            id=uuid.uuid4(),
            plan=data["plan"],
            status="pending",
            posted_at=datetime.datetime.utcnow(),
            patched_at=datetime.datetime.utcnow(),
        )


class AssessmentResultSchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = ("id", "request_id", "data", "posted_at", "_links")

    id = fields.UUID(dump_only=True)
    request_id = fields.UUID(required=True)
    data = fields.Str(required=True, validate=Length(min=1))
    posted_at = fields.DateTime(dump_only=True)
    _links = ma.Hyperlinks({
        "self":
            ma.URLFor("api.assessment_result",
                request_id="<request_id>", id="<id>"),
        "collection":
            ma.URLFor("api.all_assessment_results"),

        # TODO Only add this link if the results are available
        "data":
            ma.URLFor("api.assessment_result_zip",
                request_id="<request_id>", id="<id>"),
        "indicator_results":
            ma.URLFor("api.grouped_assessment_indicator_results",
                result_id="<id>"),
    })


    def key(self,
            many):
        return "assessment_results" if many else "assessment_result"


    @pre_load(
        pass_many=True)
    def unwrap(self,
            data,
            many):
        key = self.key(many)

        if key not in data:
            raise ValidationError("Input data must have a {} key".format(key))

        return data[key]


    @post_dump(
        pass_many=True)
    def wrap(self,
            data,
            many):
        key = self.key(many)

        return {
            key: data
        }


    @post_load
    def make_object(self,
            data):
        return AssessmentResultModel(
            id=uuid.uuid4(),
            request_id=data["request_id"],
            data=data["data"],
            posted_at=datetime.datetime.utcnow(),
        )


class AssessmentIndicatorResultSchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = (
            "id", "result_id", "difference", "statistics", "posted_at",
            "_links")

    id = fields.UUID(dump_only=True)
    result_id = fields.UUID(required=True)
    difference = fields.Str(required=True, validate=Length(min=1))
    statistics = fields.Dict(required=True)
    posted_at = fields.DateTime(dump_only=True)
    _links = ma.Hyperlinks({
        "self":
            ma.URLFor("api.assessment_indicator_result",
                result_id="<result_id>", id="<id>"),
        "collection":
            ma.URLFor("api.all_assessment_indicator_results")
    })


    def key(self,
            many):
        return "assessment_indicator_results" if many else \
            "assessment_indicator_result"


    @pre_load(
        pass_many=True)
    def unwrap(self,
            data,
            many):
        key = self.key(many)

        if key not in data:
            raise ValidationError("Input data must have a {} key".format(key))

        return data[key]


    @post_dump(
        pass_many=True)
    def wrap(self,
            data,
            many):
        key = self.key(many)

        return {
            key: data
        }


    @post_load
    def make_object(self,
            data):
        return AssessmentIndicatorResultModel(
            id=uuid.uuid4(),
            result_id=data["result_id"],
            difference=data["difference"],
            statistics=data["statistics"],
            posted_at=datetime.datetime.utcnow(),
        )
