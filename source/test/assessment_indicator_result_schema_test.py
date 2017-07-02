import datetime
import unittest
import uuid
from nc_assessment_request import create_app
from nc_assessment_request.api.schema import *


class AssessmentIndicatorResultSchemaTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True
        self.app.config["SERVER_NAME"] = "localhost"

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.schema = AssessmentIndicatorResultSchema()


    def tearDown(self):
        self.schema = None

        self.app_context.pop()


    def test_empty1(self):
        client_data = {
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "_schema": [
                "Input data must have a assessment_indicator_result key"]
        })


    def test_empty2(self):
        client_data = {
            "assessment_indicator_result": {}
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "result_id": ["Missing data for required field."],
            "difference": ["Missing data for required field."],
            "statistics": ["Missing data for required field."],
        })


    def test_invalid_values(self):
        client_data = {
            "assessment_indicator_result": {
                "result_id": "meh",
                "difference": "",
                "statistics": "mean",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "difference": ["Shorter than minimum length 1."],
            "result_id": ["Not a valid UUID."],
            "statistics": ["Not a valid mapping type."],
        })


    def test_usecase1(self):

        client_data = {
            "assessment_indicator_result": {
                "result_id": uuid.uuid4(),
                "difference": "/data/diff.map",
                "statistics": {"mean": 0.5},
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)

        self.assertTrue(hasattr(data, "id"))
        self.assertTrue(isinstance(data.id, uuid.UUID))

        self.assertTrue(hasattr(data, "result_id"))
        self.assertTrue(isinstance(data.result_id, uuid.UUID))

        self.assertTrue(hasattr(data, "difference"))
        self.assertEqual(data.difference, "/data/diff.map")

        self.assertTrue(hasattr(data, "statistics"))
        self.assertTrue(isinstance(data.statistics, dict))
        self.assertEqual(data.statistics, {"mean": 0.5})

        self.assertTrue(hasattr(data, "posted_at"))
        self.assertTrue(isinstance(data.posted_at, datetime.datetime))

        data.id = uuid.uuid4()
        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("assessment_indicator_result" in data)

        assessment_indicator_result = data["assessment_indicator_result"]

        self.assertTrue("id" in assessment_indicator_result)
        self.assertTrue("result_id" in assessment_indicator_result)
        self.assertTrue("difference" in assessment_indicator_result)
        self.assertTrue("statistics" in assessment_indicator_result)
        self.assertTrue("posted_at" in assessment_indicator_result)

        self.assertTrue("_links" in assessment_indicator_result)

        links = assessment_indicator_result["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


if __name__ == "__main__":
    unittest.main()
