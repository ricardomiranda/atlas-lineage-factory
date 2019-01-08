#!/usr/bin/python3
import pickle
import unittest

from app.lineage import lineage
from app.lineage.lineage import RequestNamedTuple
from resources import pickled_objects


class TestLineage(unittest.TestCase):

    def test_payload_given_empty_arguments_should_return_valid_dict(self):
        actual = lineage.payload(description="",
                                 inputs=[],
                                 name="",
                                 outputs=[],
                                 operation_type="",
                                 qualified_name="",
                                 type_name="")
        expected = {"description": "",
                    "inputs": [],
                    "name": "",
                    "outputs": [],
                    "operationType": "",
                    "typeName": "",
                    "qualifiedName": "",
                    "guid": -1}
        self.assertEqual(expected, actual)

    def test_payload_given_arguments_with_valid_inputs_and_outputs_dicts_should_return_valid_dict(self):
        actual = lineage.payload(description="",
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
        actual = lineage.build_request(atlas_url="", credentials={})
        expected = RequestNamedTuple(method="GET",
                                     headers={'Content-Type': 'application/json',
                                              'Accept': 'application/json;charset=UTF-8'},
                                     atlas_url="",
                                     payload={},
                                     credentials={})
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
        actual = lineage.build_request(atlas_url=atlas_url,
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
            lineage.build_request(atlas_url="http://localhost:21000/api/atlas/entities?type=hive_table"))

        pickled_expected = pickled_objects.pickled_request_hive_tables

        expected = pickle.loads(pickled_expected)

        self.assertEqual(
            [expected.method, expected.url, expected.headers, expected.body],
            [actual.method, actual.url, actual.headers, actual.body])
