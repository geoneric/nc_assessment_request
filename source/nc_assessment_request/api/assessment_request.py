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



# All results
# - Get all results
# - Post result
api_restful.add_resource(AllAssessmentResultsResource,
    "/assessment_results",
    endpoint="all_assessment_results")

# Result by request-id
# - Get assessment results by request-id
api_restful.add_resource(GroupedAssessmentResultsResource,
    "/assessment_results/<uuid:request_id>",
    endpoint="grouped_assessment_results")

# Result by id
# - Get assessment result by id
api_restful.add_resource(AssessmentResultResource,
    "/assessment_results/<uuid:request_id>/<uuid:id>",
    endpoint="assessment_result")

# Result data by id
# - Get assessment result data by id
api_restful.add_resource(AssessmentResultData,
    "/assessment_results/<uuid:request_id>/<uuid:id>/zip",
    endpoint="assessment_result_zip")


# All indicator results
# - Get all queries
# - Post assessment indicator result
api_restful.add_resource(AllAssessmentIndicatorResultsResource,
    "/assessment_indicator_results",
    endpoint="all_assessment_indicator_results")

# Indicator results grouped by result-id
# - Get assessment indicator results by result-id
api_restful.add_resource(GroupedAssessmentIndicatorResultsResource,
    "/assessment_indicator_results/<uuid:result_id>",
    endpoint="grouped_assessment_indicator_results")

# Indicator result by id
# - Get assessment indicator result by id
api_restful.add_resource(AssessmentIndicatorResultResource,
    "/assessment_indicator_results/<uuid:result_id>/<uuid:id>",
    endpoint="assessment_indicator_result")
