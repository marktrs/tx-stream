from unittest import TestCase, IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch
from flows.indexer.etherscan import get_latest_block_number, get_filtered_event_logs


class TestGetLatestBlockNumber(TestCase):
    @patch("flows.indexer.etherscan.requests")
    def test_default(self, mock_requests):
        expected_result = {
            "jsonrpc": "2.0",
            "id": 83,
            "result": "0x10ad07e",
        }
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        mock_requests.get.return_value = mock_response
        result = get_latest_block_number.fn()
        self.assertIsNotNone(result)
        self.assertEqual(result, expected_result["result"])

    @patch("flows.indexer.etherscan.requests")
    def test_invalid_request(self, mock_requests):
        with self.assertRaises(Exception) as cm:
            assert True, False
            expected_result = {
                "status": "0",
                "message": "NOTOK",
                "result": "Error! Missing Or invalid Action name",
            }
            mock_response = MagicMock()
            mock_response.json.return_value = expected_result
            mock_requests.get.return_value = mock_response
            get_latest_block_number.fn()
        self.assertEqual(
            str(cm.exception), "Error! Missing Or invalid Action name -- NOTOK"
        )


class TestGetFilteredEventLogs(IsolatedAsyncioTestCase):
    @patch("flows.indexer.etherscan.requests")
    async def test_default(self, mock_requests):
        expected_result = {
            "status": "1",
            "message": "OK",
            "result": [
                {
                    "address": "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
                    "topics": [
                        "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67",
                        "0x000000000000000000000000e592427a0aece92de3edee1f18e0157c05861564",
                        "0x000000000000000000000000e592427a0aece92de3edee1f18e0157c05861564",
                    ],
                    "data": "0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffff8dcd9a2000000000000000000000000000000000000000000000000007c58508723800000000000000000000000000000000000000042f6fac2e8d93171810499824dd6000000000000000000000000000000000000000000000000000139d797d3bfe0000000000000000000000000000000000000000000000000000000000002f9b4",
                    "blockNumber": "0xbcdb3b",
                    "blockHash": "0x058801437bd761eb140351d50fd2f0ee6c6caf9a338e2eca80c28be59f54787e",
                    "timeStamp": "0x609318e5",
                    "gasPrice": "0x10e74c1600",
                    "gasUsed": "0x39d10",
                    "logIndex": "0x49",
                    "transactionHash": "0x0804ff007263a885191f23c808a9346e62d502a1fc23be82eb14052408d76ae2",
                    "transactionIndex": "0x48",
                },
            ],
        }
        mock_response = MagicMock()
        mock_response.json.return_value = expected_result
        mock_requests.get.return_value = mock_response
        result = await get_filtered_event_logs.fn(
            contract_addr="",
            topic="",
            from_block=1,
            to_block=2,
            page=1,
            result_offset=1,
        )
        self.assertIsNotNone(result)
        self.assertEqual(result, expected_result["result"])

    @patch("flows.indexer.etherscan.requests")
    async def test_no_records(self, mock_requests):
        with self.assertRaises(AssertionError) as cm:
            mock_response = MagicMock()
            expected_result = {
                "status": "0",
                "message": "No records found",
                "result": [],
            }
            mock_response.json.return_value = expected_result
            mock_requests.get.return_value = mock_response
            await get_filtered_event_logs.fn(
                contract_addr="",
                topic="",
                from_block=1,
                to_block=2,
                page=1,
                result_offset=1,
            )
        self.assertEqual(
            str(cm.exception),
            f"[] -- No records found",
        )


if __name__ == "__main__":
    unittest.main()
