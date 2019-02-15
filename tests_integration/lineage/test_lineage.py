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

    def test_request_call_given_empty_request_error_01(self):
        actual = lineage.send_request(
            lineage.prepare_request(
                lineage.build_request_named_tuple(
                    atlas_url="http://localhost:21000/api/atlas/api/atlas/v2/entity",
                    method="POST",
                    payload=lineage.create_lineage_payload(
                        description="",
                        inputs=[{}],
                        operation_type="",
                        name="",
                        outputs=[{}],
                        qualified_name="",
                        type_name=""),
                    credentials=credentials()))).status_code

        expected = 500

        self.assertEqual(expected, actual)

    def test_request_call_given_empty_request_error_02(self):
        actual = lineage.send_request(
            lineage.prepare_request(
                lineage.build_request_named_tuple(
                    atlas_url="http://localhost:21000/api/atlas/api/atlas/v2/entity",
                    method="POST",
                    payload=lineage.create_lineage_payload(
                        description="",
                        inputs=[{
                            "guid": "0",
                            "typeName": "hive_table"}],
                        operation_type="",
                        name="",
                        outputs=[{
                            "guid": "0",
                            "typeName": "hive_table"
                        }],
                        qualified_name="",
                        type_name=""),
                    credentials=credentials()))).status_code

        expected = 500

        self.assertEqual(expected, actual)

    def test_request_call_given_empty_request_error_03(self):
        actual = lineage.send_request(
            lineage.prepare_request(
                lineage.build_request_named_tuple(
                    atlas_url="http://localhost:21000/api/atlas/api/atlas/v2/entity",
                    method="POST",
                    payload=lineage.create_lineage_payload(
                        description="loop",
                        inputs=[{
                            "guid": "eab600ff-1558-4e99-8dc7-06acb8a593b5",
                            "typeName": "hive_table"}],
                        operation_type="fake",
                        name="link",
                        outputs=[{
                            "guid": "eab600ff-1558-4e99-8dc7-06acb8a593b5",
                            "typeName": "hive_table"
                        }],
                        qualified_name="hive_tables_flow_process.link.fake",
                        type_name="hive_tables_flow_process"),
                    credentials=credentials()))).status_code

        expected = 100

        self.assertEqual(expected, actual)

        if __name__ == '__main__':
            unittest.main()
