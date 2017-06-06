#!/usr/bin/env bash
set -e


docker build -t test/nc_assessment_request .
docker run \
    --env NC_CONFIGURATION=development \
    -p5000:5000 \
    -v$(pwd)/nc_assessment_request:/nc_assessment_request \
    test/nc_assessment_request
