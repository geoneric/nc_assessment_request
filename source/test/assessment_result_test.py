import os.path
import tempfile
import unittest
import uuid
import zipfile
from flask import current_app, json
from nc_assessment_request import create_app, db
from nc_assessment_request.api.schema import *


class AssessmentResultTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True
        self.app.config["SERVER_NAME"] = "localhost"
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        self.assessment_result1 = {
            "request_id": uuid.uuid4(),
        }
        self.assessment_result2 = {
            "request_id": uuid.uuid4(),
        }
        self.assessment_result3 = {
            "request_id": uuid.uuid4(),
        }


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def post_assessment_result(self,
            data):

        response = self.client.post("/assessment_results",
            content_type="multipart/form-data",
            data=data)
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 201, "{}: {}".format(
            response.status_code, data))

        return response


    def post_assessment_results(self):

        payloads = [
            self.assessment_result1,
            self.assessment_result2
        ]


        for payload in payloads:

            with tempfile.TemporaryDirectory() as temp_directory_pathname:

                zip_filename = "assessment_result.zip"
                zip_pathname = os.path.join(temp_directory_pathname,
                    zip_filename)


                # Create zip-file with raw results
                with zipfile.ZipFile(zip_pathname, "w") as zip_file:
                    pass


                with open(zip_pathname, "rb") as zip_file:
                    data = {
                        "data": json.dumps(payload),
                        "result": (zip_file, zip_filename)
                    }

                    self.post_assessment_result(data)


    def test_get_all_assessment_results1(self):
        # No assessment_results posted.
        response = self.client.get("/assessment_results")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("assessment_results" in data)
        self.assertEqual(data["assessment_results"], [])


    def test_get_all_assessment_results2(self):
        # Some assessment_results posted.
        self.post_assessment_results()

        response = self.client.get("/assessment_results")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("assessment_results" in data)

        assessment_results = data["assessment_results"]

        self.assertEqual(len(assessment_results), 2)


    def test_get_assessment_result(self):
        self.post_assessment_results()

        response = self.client.get("/assessment_results")
        data = response.data.decode("utf8")
        data = json.loads(data)
        assessment_results = data["assessment_results"]
        assessment_result = assessment_results[0]
        uri = assessment_result["_links"]["self"]
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("assessment_result" in data)

        assessment_result = data["assessment_result"]

        self.assertEqual(data["assessment_result"], assessment_result)

        self.assertTrue("id" in assessment_result)
        self.assertTrue(isinstance(assessment_result["id"], str))

        self.assertTrue("request_id" in assessment_result)
        self.assertTrue(isinstance(assessment_result["request_id"], str))

        self.assertTrue("data" in assessment_result)
        self.assertTrue(os.path.isfile(assessment_result["data"]))

        self.assertTrue("posted_at" in assessment_result)

        self.assertTrue("_links" in assessment_result)

        links = assessment_result["_links"]

        self.assertTrue("self" in links)
        self.assertEqual(links["self"], uri)

        self.assertTrue("collection" in links)
        self.assertTrue("indicator_results" in links)
        self.assertTrue("data" in links)


    def test_get_unexisting_assessment_result(self):
        self.post_assessment_results()

        response = self.client.get("/assessment_results")
        data = response.data.decode("utf8")
        data = json.loads(data)
        assessment_results = data["assessment_results"]
        assessment_result = assessment_results[0]
        uri = assessment_result["_links"]["self"]
        # Invalidate uri
        uri = os.path.join(os.path.split(uri)[0], str(uuid.uuid4()))
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_assessment_result(self):

        with tempfile.TemporaryDirectory() as temp_directory_pathname:

            zip_filename = "assessment_result.zip"
            zip_pathname = os.path.join(temp_directory_pathname,
                zip_filename)


            # Create zip-file with raw results
            with zipfile.ZipFile(zip_pathname, "w") as zip_file:
                pass


            with open(zip_pathname, "rb") as zip_file:
                data = {
                    "data": json.dumps(self.assessment_result3),
                    "result": (zip_file, zip_filename)
                }

                response = self.post_assessment_result(data)


        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 201, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("assessment_result" in data)

        assessment_result = data["assessment_result"]

        self.assertTrue("id" in assessment_result)
        self.assertTrue(isinstance(assessment_result["id"], str))

        self.assertTrue("request_id" in assessment_result)
        self.assertEqual(assessment_result["request_id"],
            str(self.assessment_result3["request_id"]))

        self.assertTrue("data" in assessment_result)
        self.assertTrue(os.path.isfile(assessment_result["data"]))

        self.assertTrue("posted_at" in assessment_result)

        self.assertTrue("_links" in assessment_result)

        links = assessment_result["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)
        self.assertTrue("indicator_results" in links)
        self.assertTrue("data" in links)


    def test_delete_assessment_result(self):

        with tempfile.TemporaryDirectory() as temp_directory_pathname:

            zip_filename = "assessment_result.zip"
            zip_pathname = os.path.join(temp_directory_pathname,
                zip_filename)


            # Create zip-file with raw results
            with zipfile.ZipFile(zip_pathname, "w") as zip_file:
                pass


            with open(zip_pathname, "rb") as zip_file:
                data = {
                    "data": json.dumps(self.assessment_result3),
                    "result": (zip_file, zip_filename)
                }

                response = self.post_assessment_result(data)


        data = response.data.decode("utf8")
        data = json.loads(data)
        assessment_result = data["assessment_result"]
        links = assessment_result["_links"]
        self_uri = links["self"]

        response = self.client.delete(self_uri)
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 204)


    def test_post_bad_request(self):
        response = self.client.post("/assessment_results")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_unprocessable_entity(self):
        payload = ""
        response = self.client.post("/assessment_results",
            data=json.dumps({"assessment_result": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


if __name__ == "__main__":
    unittest.main()
