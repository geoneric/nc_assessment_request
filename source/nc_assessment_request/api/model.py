from sqlalchemy_utils import UUIDType
from .. import db


class AssessmentRequestModel(db.Model):
    id = db.Column(UUIDType(), primary_key=True)
    plan = db.Column(db.UnicodeText)
    status = db.Column(db.Unicode(40))
    posted_at = db.Column(db.DateTime)
    patched_at = db.Column(db.DateTime)
