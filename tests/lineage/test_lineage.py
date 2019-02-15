#!/usr/bin/python3
import json
import pathlib
import pickle
import unittest

from app.lineage import lineage
from app.lineage.lineage import RequestNamedTuple
from resources import pickled_objects


def credentials():
    auth_file = pathlib.Path(pathlib.Path(__file__).parent, "../../resources/auth.json")
    with auth_file.open() as f:
        auth = json.loads(f.read())

    return (auth["user"], auth["password"])


class TestLineage(unittest.TestCase):

    def test_payload_given_empty_arguments_should_return_valid_dict(self):
        actual = lineage.create_lineage_payload(
            description="",
            inputs=[{}],
            name="",
            outputs=[{}],
            operation_type="",
            qualified_name="",
            type_name="")
        expected = {"description": "",
                    "inputs": [{}],
                    "name": "",
                    "outputs": [{}],
                    "operationType": "",
                    "typeName": "",
                    "qualifiedName": "",
                    "guid": -1}
        self.assertEqual(expected, actual)

    def test_payload_given_arguments_with_valid_inputs_and_outputs_dicts_should_return_valid_dict(self):
        actual = lineage.create_lineage_payload(
            description="",
            inputs=[{
                "guid": "dc50d05c-2fbe-481b-ac6f-0180f1414fb5",
                "typeName": "hive_table"
            }],
            name="",
            outputs=[{
                "guid": "dc50d05c-2fbe-481b-ac6f-0180f1414fb5",
                "typeName": "hive_table"
            }],
            operation_type="",
            qualified_name="",
            type_name="")
        expected = {"description": "",
                    "inputs": [{
                        "guid": "dc50d05c-2fbe-481b-ac6f-0180f1414fb5",
                        "typeName": "hive_table"
                    }],
                    "name": "",
                    "outputs": [{
                        "guid": "dc50d05c-2fbe-481b-ac6f-0180f1414fb5",
                        "typeName": "hive_table"
                    }],
                    "operationType": "",
                    "typeName": "",
                    "qualifiedName": "",
                    "guid": -1}
        self.assertEqual(expected, actual)

    def test_build_request_given_empty_arguments_should_return_empty_object(self):
        actual = lineage.build_request_named_tuple(atlas_url="", credentials=("", ""))
        expected = RequestNamedTuple(method="GET",
                                     headers={"Content-Type": "application/json",
                                              "Accept": "application/json;charset=UTF-8"},
                                     atlas_url="",
                                     payload={},
                                     credentials=("", ""))
        self.assertEqual(expected, actual)

    def test_build_request_given_valid_arguments_should_return_valid_object(self):
        payload = {"description": "",
                   "inputs": [{
                       "guid": "dc50d05c-2fbe-481b-ac6f-0180f1414fb5",
                       "typeName": "hive_table"
                   }],
                   "name": "",
                   "outputs": [{
                       "guid": "dc50d05c-2fbe-481b-ac6f-0180f1414fb5",
                       "typeName": "hive_table"
                   }],
                   "operationType": "",
                   "typeName": "",
                   "qualifiedName": "",
                   "guid": -1}
        atlas_url = "http://localhost:21000/api/atlas/types"
        credentials = {"user": "admin:admin"}
        actual = lineage.build_request_named_tuple(atlas_url=atlas_url,
                                                   payload=payload, credentials=credentials)
        expected = RequestNamedTuple(method="GET",
                                     headers={'Content-Type': 'application/json',
                                              'Accept': 'application/json;charset=UTF-8'},
                                     atlas_url=atlas_url,
                                     payload=payload,
                                     credentials=credentials)
        self.assertEqual(expected, actual)

    def test_request_call_given_empty_request_named_tuple_should_return_request_object(self):
        actual = lineage.prepare_request(
            lineage.build_request_named_tuple(
                atlas_url="http://localhost:21000/api/atlas/entities?type=hive_table",
                credentials=credentials()))

        expected = pickle.loads(pickled_objects.pickled_request_hive_tables)

        self.assertEqual(
            [expected.method, expected.url, expected.headers, expected.body],
            [actual.method, actual.url, actual.headers, actual.body])

    def test_create_lineage_prepare_empty_data(self):
        actual = lineage.create_lineage_prepare(
            atlas_url="http://localhost:21000/api/atlas",
            description="",
            inputs=[{}],
            operation_type="",
            name="",
            outputs=[{}],
            type_name="",
            credentials=credentials())

        expected = pickle.loads(pickled_objects.pickled_request_empty_data)

        self.assertEqual(
            [expected.method, expected.url, expected.headers, expected.body],
            [actual.method, actual.url, actual.headers, actual.body])

    def test_create_lineage_prepare_error_01(self):
        # actual = pickle.dumps(lineage.create_lineage_prepare(
        actual = lineage.create_lineage_prepare(
            description="Data flow form raw to canonical data model",
            inputs=[{}],
            operation_type="Spark",
            name="data_mapping",
            outputs=[{}],
            atlas_url="http://localhost:21000/api/atlas",
            type_name="hive_tables_flow_process")

        # )

        expected = pickle.loads(pickled_objects.pickled_request_error_01)

        # self.assertEqual(expected, actual)
        self.assertEqual(
            [expected.method, expected.url, expected.headers, expected.body],
            [actual.method, actual.url, actual.headers, actual.body])


if __name__ == '__main__':
    unittest.main()
