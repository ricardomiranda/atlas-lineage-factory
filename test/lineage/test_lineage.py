#!/usr/bin/python3
import pickle
import unittest

from app.lineage import lineage
from app.lineage.lineage import RequestNamedTuple


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
        self.assertEquals(expected, actual)

    def test_request_call_given_empty_request_named_tuple_should_return_request_object(self):
        expected = lineage.prepare_request_object(
            lineage.build_request(atlas_url="http://localhost:21000/api/atlas/entities?type=hive_table"))

        pickled_actual = (b'\x80\x03crequests.models\nPreparedRequest\nq\x00)\x81q\x01}q\x02(X\x06\x00'
                           b'\x00\x00methodq\x03X\x03\x00\x00\x00GETq\x04X\x03\x00\x00\x00urlq\x05X9'
                           b'\x00\x00\x00http://localhost:21000/api/atlas/entities?type=hive_table'
                           b'q\x06X\x07\x00\x00\x00headersq\x07crequests.structures\nCaseInsensitiveDict'
                           b'\nq\x08)\x81q\t}q\nX\x06\x00\x00\x00_storeq\x0bccollections\nOrderedDict\n'
                           b'q\x0c)Rq\r(X\x0c\x00\x00\x00content-typeq\x0eX\x0c\x00\x00\x00Content-Typeq'
                           b'\x0fX\x10\x00\x00\x00application/jsonq\x10\x86q\x11X\x06\x00\x00\x00acce'
                           b'ptq\x12X\x06\x00\x00\x00Acceptq\x13X\x1e\x00\x00\x00application/json;chars'
                           b'et=UTF-8q\x14\x86q\x15X\x0e\x00\x00\x00content-lengthq\x16X\x0e\x00\x00\x00C'
                           b'ontent-Lengthq\x17X\x01\x00\x00\x002q\x18\x86q\x19X\r\x00\x00\x00authoriza'
                           b'tionq\x1aX\r\x00\x00\x00Authorizationq\x1bX\x1e\x00\x00\x00Basic YWRtaW46aG9'
                           b'ydG9ud29ya3Mxq\x1c\x86q\x1dusbX\x08\x00\x00\x00_cookiesq\x1ecrequests.cookie'
                           b's\nRequestsCookieJar\nq\x1f)\x81q }q!(X\x07\x00\x00\x00_policyq"chttp.cookie'
                           b'jar\nDefaultCookiePolicy\nq#)\x81q$}q%(X\x08\x00\x00\x00netscapeq&\x88X\x07'
                           b"\x00\x00\x00rfc2965q'\x89X\x13\x00\x00\x00rfc2109_as_netscapeq(N"
                           b'X\x0c\x00\x00\x00hide_cookie2q)\x89X\r\x00\x00\x00strict_domainq*'
                           b'\x89X\x1b\x00\x00\x00strict_rfc2965_unverifiableq+\x88X\x16\x00\x00\x00str'
                           b'ict_ns_unverifiableq,\x89X\x10\x00\x00\x00strict_ns_domainq-K\x00X'
                           b'\x1c\x00\x00\x00strict_ns_set_initial_dollarq.\x89X\x12\x00\x00\x00strict_n'
                           b's_set_pathq/\x89X\x10\x00\x00\x00_blocked_domainsq0)X\x10\x00\x00\x00_allow'
                           b'ed_domainsq1NX\x04\x00\x00\x00_nowq2JX\x150\\ubh\x1e}q3h2JX\x150\\u'
                           b'bX\x04\x00\x00\x00bodyq4C\x02{}q5X\x05\x00\x00\x00hooksq6}q7X\x08\x00'
                           b'\x00\x00responseq8]q9sX\x0e\x00\x00\x00_body_positionq:Nub.')

        actual = pickle.loads(pickled_actual)

        self.assertEqual(
            [expected.method, expected.url, expected.headers, expected.body],
            [actual.method, actual.url, actual.headers, actual.body])

