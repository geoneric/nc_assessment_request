from . import api_restful
from .resource import *


# - Get all assessment requests
# - Post assessment request
api_restful.add_resource(AssessmentRequestsResource,
    "/assessment_requests",
    endpoint="assessment_requests")


# - Get assessment request by id
api_restful.add_resource(AssessmentRequestResource,
    "/assessment_requests/<uuid:id>",
    endpoint="assessment_request")
