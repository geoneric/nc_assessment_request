import os
from nc_assessment_request import create_app

os.environ["NC_CONFIGURATION"] = \
    os.environ.get("NC_CONFIGURATION") or "production"
app = create_app(os.getenv("NC_CONFIGURATION"))
