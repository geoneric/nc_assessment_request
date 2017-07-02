from sqlalchemy_utils import JSONType, UUIDType
from .. import db


class AssessmentRequestModel(db.Model):

    id = db.Column(UUIDType(), primary_key=True)

    # Uri to plan resource to assess
    plan = db.Column(db.UnicodeText)

    status = db.Column(db.Unicode(40))
    posted_at = db.Column(db.DateTime)
    patched_at = db.Column(db.DateTime)


class AssessmentResultModel(db.Model):

    id = db.Column(UUIDType(), primary_key=True)

    # Id of request resource we are part of
    # TODO This is a foreign key. Use it!
    request_id = db.Column(UUIDType())

    # Pointer to dataset/zip with all raw results
    data = db.Column(db.UnicodeText)

    posted_at = db.Column(db.DateTime)


class AssessmentIndicatorResultModel(db.Model):

    id = db.Column(UUIDType(), primary_key=True)

    # Id of result resource we are part of
    result_id = db.Column(UUIDType())

    # WCS Layer name of map showing differences
    difference = db.Column(db.UnicodeText)

    # JSON snippet with some statistics
    statistics = db.Column(JSONType)

    posted_at = db.Column(db.DateTime)
