import datetime
import unittest
import uuid
from nc_assessment_request import create_app
from nc_assessment_request.api.schema import *


class AssessmentRequestSchemaTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True
        self.app.config["SERVER_NAME"] = "localhost"

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.schema = AssessmentRequestSchema()


    def tearDown(self):
        self.schema = None

        self.app_context.pop()


    def test_empty1(self):
        client_data = {
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "_schema": ["Input data must have a assessment_request key"]
        })


    def test_empty2(self):
        client_data = {
            "assessment_request": {}
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "plan": ["Missing data for required field."],
        })


    def test_invalid_plan(self):
        client_data = {
            "assessment_request": {
                "plan": "",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "plan": ["Shorter than minimum length 1."],
        })


    def test_usecase1(self):

        client_data = {
            "assessment_request": {
                "plan": "plans/plan_a",
            }
        }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)

        self.assertTrue(hasattr(data, "id"))
        self.assertTrue(isinstance(data.id, uuid.UUID))

        self.assertTrue(hasattr(data, "plan"))
        self.assertEqual(data.plan, "plans/plan_a")

        self.assertTrue(hasattr(data, "status"))
        self.assertEqual(data.status, "pending")

        self.assertTrue(hasattr(data, "posted_at"))
        self.assertTrue(isinstance(data.posted_at, datetime.datetime))

        self.assertTrue(hasattr(data, "patched_at"))
        self.assertTrue(isinstance(data.patched_at, datetime.datetime))

        data.id = uuid.uuid4()
        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("assessment_request" in data)

        assessment_request = data["assessment_request"]

        self.assertTrue("id" in assessment_request)
        self.assertTrue("plan" in assessment_request)
        self.assertTrue("status" in assessment_request)
        self.assertTrue("posted_at" in assessment_request)
        self.assertTrue("patched_at" in assessment_request)

        self.assertTrue("_links" in assessment_request)

        links = assessment_request["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)
        self.assertFalse("result" in links)


if __name__ == "__main__":
    unittest.main()
