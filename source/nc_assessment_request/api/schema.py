import datetime
import uuid
from marshmallow import fields, post_dump, post_load, pre_load, ValidationError
from marshmallow.validate import Length, OneOf
from .. import ma
from .model import *


class AssessmentRequestSchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = (
            "id", "user", "pathname", "status",
            "posted_at", "patched_at", "_links"
        )

    id = fields.UUID(dump_only=True)
    user = fields.UUID(required=True)
    status = fields.Str(dump_only=True,
        validate=OneOf(["pending", "queued", "executing", "failed",
            "succeeded"]))
    pathname = fields.Str(dump_only=True)
    posted_at = fields.DateTime(dump_only=True)
    patched_at = fields.DateTime(dump_only=True)
    _links = ma.Hyperlinks({
        "self": ma.URLFor("api.assessment_request", id="<id>"),
        "collection": ma.URLFor("api.assessment_requests", id="<id>")
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
        return AssessmentRequestModel(
            id=uuid.uuid4(),
            user=data["user"],
            status="pending",
            posted_at=datetime.datetime.utcnow(),
            patched_at=datetime.datetime.utcnow(),
        )
