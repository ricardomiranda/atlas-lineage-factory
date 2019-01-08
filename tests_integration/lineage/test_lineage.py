#!/usr/bin/python3
import unittest

from app.lineage import lineage


class TestIntegrationLineage(unittest.TestCase):

    def test_request_call_given_empty_request_named_tuple_should_return_request_object(self):
        actual = lineage.send_request(
            lineage.prepare_request(
                lineage.build_request(
                    atlas_url="http://localhost:21000/api/atlas/entities?type=hive_table"))).status_code

        expected = 200

        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
