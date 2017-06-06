from sqlalchemy_utils import JSONType, UUIDType
from .. import db


class AssessmentRequestModel(db.Model):
    id = db.Column(UUIDType(), primary_key=True)
    user = db.Column(UUIDType())
    status = db.Column(db.Unicode(40))
    pathname = db.Column(db.UnicodeText)
    posted_at = db.Column(db.DateTime)
    patched_at = db.Column(db.DateTime)
