import os.path
import unittest
import uuid
from flask import current_app, json
from nc_assessment_request import create_app, db
from nc_assessment_request.api.schema import *


class AssessmentIndicatorResultTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True
        self.app.config["SERVER_NAME"] = "localhost"
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        self.assessment_indicator_result1 = {
            "result_id": uuid.uuid4(),
            "difference": "datas/data_a",
            "statistics": {"mean": 0.5},
        }
        self.assessment_indicator_result2 = {
            "result_id": uuid.uuid4(),
            "difference": "datas/data_b",
            "statistics": {"mean": 0.6},
        }
        self.assessment_indicator_result3 = {
            "result_id": uuid.uuid4(),
            "difference": "datas/data_c",
            "statistics": {"mean": 0.7},
        }


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def post_assessment_indicator_result(self,
            payload):

        response = self.client.post("/assessment_indicator_results",
            data=json.dumps({"assessment_indicator_result": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 201, "{}: {}".format(
            response.status_code, data))

        return response


    def post_assessment_indicator_results(self):

        payloads = [
            self.assessment_indicator_result1,
            self.assessment_indicator_result2
        ]

        for payload in payloads:
            self.post_assessment_indicator_result(payload)


    def test_get_all_assessment_indicator_results1(self):
        # No assessment_indicator_results posted.
        response = self.client.get("/assessment_indicator_results")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("assessment_indicator_results" in data)
        self.assertEqual(data["assessment_indicator_results"], [])


    def test_get_all_assessment_indicator_results2(self):
        # Some assessment_indicator_results posted.
        self.post_assessment_indicator_results()

        response = self.client.get("/assessment_indicator_results")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("assessment_indicator_results" in data)

        assessment_indicator_results = data["assessment_indicator_results"]

        self.assertEqual(len(assessment_indicator_results), 2)


    def test_get_assessment_indicator_result(self):
        self.post_assessment_indicator_results()

        response = self.client.get("/assessment_indicator_results")
        data = response.data.decode("utf8")
        data = json.loads(data)
        assessment_indicator_results = data["assessment_indicator_results"]
        assessment_indicator_result = assessment_indicator_results[0]
        uri = assessment_indicator_result["_links"]["self"]
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("assessment_indicator_result" in data)

        assessment_indicator_result = data["assessment_indicator_result"]

        self.assertEqual(data["assessment_indicator_result"],
            assessment_indicator_result)

        self.assertTrue("id" in assessment_indicator_result)
        self.assertTrue(isinstance(assessment_indicator_result["id"], str))

        self.assertTrue("result_id" in assessment_indicator_result)
        self.assertTrue(isinstance(assessment_indicator_result["result_id"],
            str))

        self.assertTrue("difference" in assessment_indicator_result)
        self.assertEqual(assessment_indicator_result["difference"],
            self.assessment_indicator_result1["difference"])

        self.assertTrue("statistics" in assessment_indicator_result)
        self.assertEqual(assessment_indicator_result["statistics"],
            self.assessment_indicator_result1["statistics"])

        self.assertTrue("posted_at" in assessment_indicator_result)

        self.assertTrue("_links" in assessment_indicator_result)

        links = assessment_indicator_result["_links"]

        self.assertTrue("self" in links)
        self.assertEqual(links["self"], uri)

        self.assertTrue("collection" in links)


    def test_get_unexisting_assessment_indicator_result(self):
        self.post_assessment_indicator_results()

        response = self.client.get("/assessment_indicator_results")
        data = response.data.decode("utf8")
        data = json.loads(data)
        assessment_indicator_results = data["assessment_indicator_results"]
        assessment_indicator_result = assessment_indicator_results[0]
        uri = assessment_indicator_result["_links"]["self"]
        # Invalidate uri
        uri = os.path.join(os.path.split(uri)[0], str(uuid.uuid4()))
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_assessment_indicator_result(self):
        response = self.post_assessment_indicator_result(
            self.assessment_indicator_result3)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 201, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("assessment_indicator_result" in data)

        assessment_indicator_result = data["assessment_indicator_result"]

        self.assertTrue("id" in assessment_indicator_result)
        self.assertTrue(isinstance(assessment_indicator_result["id"], str))

        self.assertTrue("result_id" in assessment_indicator_result)
        self.assertEqual(assessment_indicator_result["result_id"],
            str(self.assessment_indicator_result3["result_id"]))

        self.assertTrue("difference" in assessment_indicator_result)
        self.assertEqual(assessment_indicator_result["difference"],
            self.assessment_indicator_result3["difference"])

        self.assertTrue("statistics" in assessment_indicator_result)
        self.assertEqual(assessment_indicator_result["statistics"],
            self.assessment_indicator_result3["statistics"])

        self.assertTrue("posted_at" in assessment_indicator_result)

        self.assertTrue("_links" in assessment_indicator_result)

        links = assessment_indicator_result["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


    def test_delete_assessment_indicator_result(self):
        response = self.post_assessment_indicator_result(
            self.assessment_indicator_result3)
        data = response.data.decode("utf8")
        data = json.loads(data)
        assessment_indicator_result = data["assessment_indicator_result"]
        links = assessment_indicator_result["_links"]
        self_uri = links["self"]

        response = self.client.delete(self_uri)
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 204)


    def test_post_bad_request(self):
        response = self.client.post("/assessment_indicator_results")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_unprocessable_entity(self):
        payload = ""
        response = self.client.post("/assessment_indicator_results",
            data=json.dumps({"assessment_indicator_result": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 422, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


if __name__ == "__main__":
    unittest.main()
