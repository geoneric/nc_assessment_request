import os.path
import unittest
import uuid
from flask import current_app, json
from nc_assessment_request import create_app, db
from nc_assessment_request.api.schema import *


class AssessmentRequestTestCase(unittest.TestCase):

    pass


    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True
        self.app.config["SERVER_NAME"] = "localhost"
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        self.assessment_request1 = {
            "plan": "plans/plan_a",
        }
        self.assessment_request2 = {
            "plan": "plans/plan_b",
        }
        self.assessment_request3 = {
            "plan": "plans/plan_c",
        }


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def post_assessment_request(self,
            payload):

        response = self.client.post("/assessment_requests",
            data=json.dumps({"assessment_request": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 201, "{}: {}".format(
            response.status_code, data))

        return response


    def post_assessment_requests(self):

        payloads = [
            {
                "plan": self.assessment_request1["plan"],
            },
            {
                "plan": self.assessment_request2["plan"],
            },
        ]

        for payload in payloads:
            self.post_assessment_request(payload)


    def test_get_all_assessment_requests1(self):
        # No assessment_requests posted.
        response = self.client.get("/assessment_requests")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("assessment_requests" in data)
        self.assertEqual(data["assessment_requests"], [])


    def test_get_all_assessment_requests2(self):
        # Some assessment_requests posted.
        self.post_assessment_requests()

        response = self.client.get("/assessment_requests")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("assessment_requests" in data)

        assessment_requests = data["assessment_requests"]

        self.assertEqual(len(assessment_requests), 2)


    def test_get_assessment_request(self):
        self.post_assessment_requests()

        response = self.client.get("/assessment_requests")
        data = response.data.decode("utf8")
        data = json.loads(data)
        assessment_requests = data["assessment_requests"]
        assessment_request = assessment_requests[0]
        uri = assessment_request["_links"]["self"]
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("assessment_request" in data)

        assessment_request = data["assessment_request"]

        self.assertEqual(data["assessment_request"], assessment_request)

        self.assertTrue("id" in assessment_request)
        self.assertTrue(isinstance(assessment_request["id"], str))

        self.assertTrue("plan" in assessment_request)
        self.assertEqual(assessment_request["plan"],
            str(self.assessment_request1["plan"]))

        self.assertTrue("status" in assessment_request)
        self.assertEqual(assessment_request["status"], "pending")

        self.assertTrue("posted_at" in assessment_request)
        self.assertTrue("patched_at" in assessment_request)

        self.assertTrue("_links" in assessment_request)

        links = assessment_request["_links"]

        self.assertTrue("self" in links)
        self.assertEqual(links["self"], uri)

        self.assertTrue("collection" in links)


    def test_get_unexisting_assessment_request(self):
        self.post_assessment_requests()

        response = self.client.get("/assessment_requests")
        data = response.data.decode("utf8")
        data = json.loads(data)
        assessment_requests = data["assessment_requests"]
        assessment_request = assessment_requests[0]
        uri = assessment_request["_links"]["self"]
        # Invalidate uri
        uri = os.path.join(os.path.split(uri)[0], str(uuid.uuid4()))
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_assessment_request(self):
        response = self.post_assessment_request(self.assessment_request3)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 201, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("assessment_request" in data)

        assessment_request = data["assessment_request"]

        self.assertTrue("id" in assessment_request)
        self.assertTrue(isinstance(assessment_request["id"], str))

        self.assertTrue("plan" in assessment_request)
        self.assertEqual(assessment_request["plan"],
            str(self.assessment_request3["plan"]))

        self.assertTrue("status" in assessment_request)
        self.assertEqual(assessment_request["status"], "pending")

        self.assertTrue("posted_at" in assessment_request)
        self.assertTrue("patched_at" in assessment_request)

        self.assertTrue("_links" in assessment_request)

        links = assessment_request["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


    def test_patch_assessment_request(self):
        response = self.post_assessment_request(self.assessment_request3)
        data = response.data.decode("utf8")
        data = json.loads(data)
        assessment_request = data["assessment_request"]
        links = assessment_request["_links"]
        self_uri = links["self"]

        payload = {
            "status": "finished"
        }

        response = self.client.patch(self_uri,
            data=json.dumps(payload), content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        assessment_request = json.loads(data)["assessment_request"]

        self.assertTrue("status" in assessment_request)
        self.assertEqual(assessment_request["status"], "finished")


    def test_delete_assessment_request(self):
        response = self.post_assessment_request(self.assessment_request3)
        data = response.data.decode("utf8")
        data = json.loads(data)
        assessment_request = data["assessment_request"]
        links = assessment_request["_links"]
        self_uri = links["self"]

        response = self.client.delete(self_uri)
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 204)


    def test_post_bad_request(self):
        response = self.client.post("/assessment_requests")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_unprocessable_entity(self):
        payload = ""
        response = self.client.post("/assessment_requests",
            data=json.dumps({"assessment_request": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 422, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


if __name__ == "__main__":
    unittest.main()
