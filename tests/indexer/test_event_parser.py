from unittest import TestCase
from unittest.mock import MagicMock
from flows.indexer.event_parser import parse


class TestParse(TestCase):
    def test_default(self):
        expected_result = {
            "jsonrpc": "2.0",
            "id": 83,
            "result": "0x10ad07e",
        }

        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        parse_result = parse(mock_response)
        self.assertEqual(parse_result, expected_result["result"])

    def test_invalid_request(self):
        with self.assertRaises(Exception) as cm:
            expected_result = {
                "status": "0",
                "message": "NOTOK",
                "result": "Error! Missing Or invalid Action name",
            }

            mock_response = MagicMock()
            mock_response.json.return_value = expected_result
            parse(mock_response)
        self.assertEqual(
            str(cm.exception), "Error! Missing Or invalid Action name -- NOTOK"
        )
