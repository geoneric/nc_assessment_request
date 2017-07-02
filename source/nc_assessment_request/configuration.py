import os
import tempfile


class Configuration:

    # Flask
    SECRET_KEY = os.environ.get("NC_ASSESSMENT_REQUEST_SECRET_KEY") or \
        "yabbadabbadoo!"
    JSON_AS_ASCII = False

    UPLOADS_DEFAULT_DEST = \
        os.environ.get("NC_UPLOADS_DEFAULT_DEST") or \
        tempfile.gettempdir()

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    DEBUG = True
    DEBUG_TOOLBAR_ENABLED = True
    FLASK_DEBUG_DISABLE_STRICT = True

    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("NC_ASSESSMENT_REQUEST_DEV_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(),
            "assessment_request-dev.sqlite")


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        from flask_debug import Debug
        Debug(app)


class TestConfiguration(Configuration):

    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("NC_ASSESSMENT_REQUEST_TEST_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(),
            "assessment_request-test.sqlite")


class ProductionConfiguration(Configuration):

    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("NC_ASSESSMENT_REQUEST_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(),
            "assessment_request.sqlite")


configuration = {
    "development": DevelopmentConfiguration,
    "test": TestConfiguration,
    "acceptance": ProductionConfiguration,
    "production": ProductionConfiguration
}
