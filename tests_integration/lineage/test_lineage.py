#!/usr/bin/python3
import json
import pathlib
import unittest

from app.lineage import lineage

def credentials():
    auth_file = pathlib.Path(pathlib.Path(__file__).parent, "../../resources/auth.json")
    with auth_file.open() as f:
        auth = json.loads(f.read())

    return (auth["user"], auth["password"])

class TestIntegrationLineage(unittest.TestCase):

    def test_request_call_given_no_credentials(self):
        actual = lineage.send_request(
            lineage.prepare_request(
                lineage.build_request_named_tuple(
                    atlas_url="http://localhost:21000/api/atlas/entities?type=hive_table"))).status_code

        expected = 401

        self.assertEqual(expected, actual)

    def test_request_call_given_with_credentials(self):
        actual = lineage.send_request(
            lineage.prepare_request(
                lineage.build_request_named_tuple(
                    atlas_url="http://localhost:21000/api/atlas/entities?type=hive_table",
                    credentials=credentials()))).status_code

        expected = 200

        self.assertEqual(expected, actual)

    def test_request_call_given_empty_request_named_tuple2(self):
        actual = lineage.send_request(
            lineage.prepare_request(
                lineage.build_request_named_tuple(
                    atlas_url="http://localhost:21000/api/atlas/no_api"))).reason

        expected = 200

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
