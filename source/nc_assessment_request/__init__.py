from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import starling.flask.error_handler
from .configuration import configuration


db = SQLAlchemy()
ma = Marshmallow()


def create_app(
        configuration_name):
    app = Flask(__name__)
    configuration_ = configuration[configuration_name]
    app.config.from_object(configuration_)
    configuration_.init_app(app)

    starling.flask.error_handler.register(app)


    # Order matters.
    db.init_app(app)
    ma.init_app(app)


    # Attach routes and custom error pages.
    from .api import api_blueprint
    app.register_blueprint(api_blueprint)


    with app.app_context():
        # http://stackoverflow.com/questions/19437883/when-scattering-flask-models-runtimeerror-application-not-registered-on-db-w
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block.
        db.create_all()


    return app
