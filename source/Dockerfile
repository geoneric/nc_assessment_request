FROM posbank.geoneric.eu:5000/nca/nc_base:latest

MAINTAINER Kor de Jong <k.dejong@geoneric.eu>

COPY requirements.txt /

RUN \
    pip install -r requirements.txt

COPY cmd.sh server.py server_flask.py uwsgi.ini /
COPY nc_assessment_request /nc_assessment_request
COPY test /test

CMD ["/cmd.sh"]
