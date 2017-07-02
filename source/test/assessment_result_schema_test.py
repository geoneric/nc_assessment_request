import datetime
import unittest
import uuid
from nc_assessment_request import create_app
from nc_assessment_request.api.schema import *


class AssessmentResultSchemaTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True
        self.app.config["SERVER_NAME"] = "localhost"

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.schema = AssessmentResultSchema()


    def tearDown(self):
        self.schema = None

        self.app_context.pop()


    def test_empty1(self):
        client_data = {
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "_schema": ["Input data must have a assessment_result key"]
        })


    def test_empty2(self):
        client_data = {
            "assessment_result": {}
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "data": ["Missing data for required field."],
            "request_id": ["Missing data for required field."],
        })


    def test_invalid_request_id(self):
        client_data = {
            "assessment_result": {
                "request_id": "meh",
                "data": "/blah/blah",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "request_id": ["Not a valid UUID."],
        })


    def test_invalid_data(self):
        client_data = {
            "assessment_result": {
                "request_id": uuid.uuid4(),
                "data": "",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "data": ["Shorter than minimum length 1."],
        })


    def test_usecase1(self):

        client_data = {
            "assessment_result": {
                "request_id": uuid.uuid4(),
                "data": "datas/data_a",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)

        self.assertTrue(hasattr(data, "id"))
        self.assertTrue(isinstance(data.id, uuid.UUID))

        self.assertTrue(hasattr(data, "request_id"))
        self.assertTrue(isinstance(data.request_id, uuid.UUID))

        self.assertTrue(hasattr(data, "data"))
        self.assertEqual(data.data, "datas/data_a")

        self.assertTrue(hasattr(data, "posted_at"))
        self.assertTrue(isinstance(data.posted_at, datetime.datetime))

        data.id = uuid.uuid4()
        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("assessment_result" in data)

        assessment_result = data["assessment_result"]

        self.assertTrue("id" in assessment_result)
        self.assertTrue("request_id" in assessment_result)
        self.assertTrue("data" in assessment_result)
        self.assertTrue("posted_at" in assessment_result)

        self.assertTrue("_links" in assessment_result)

        links = assessment_result["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)
        self.assertTrue("data" in links)
        self.assertTrue("indicator_results" in links)


if __name__ == "__main__":
    unittest.main()
