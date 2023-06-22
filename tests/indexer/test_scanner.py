import pytest

from unittest import IsolatedAsyncioTestCase, skip
from unittest.mock import patch, MagicMock
from flows.indexer.scanner import concurrent_scan
from prefect.testing.utilities import prefect_test_harness


@pytest.fixture(autouse=True, scope="session")
def prefect_test_fixture():
    with prefect_test_harness():
        yield


class TestConcurrentScan(IsolatedAsyncioTestCase):
    @skip("TODO: mock etherscan / store")
    # @patch("flows.indexer.store.AsyncPostgrestClient")
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

        # mock_store.upsert_event_logs = AsyncMock()
        # mock_store.upsert_event_logs.return_value = None

        await concurrent_scan(
            symbols="WETH_USDC",
            max_calls=5,
            pool_addr="0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8",
            start_block=1,
            latest_block=10,
            block_confirmation=5,
            block_range=5,
            event_topic="0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67",
            result_offset=5,
        )

    async def test_exceed_confirmation_blocks(self):
        start_block = 10
        latest_block = 10
        block_confirmation = 5

        await concurrent_scan(
            symbols="WETH_USDC",
            max_calls=5,
            pool_addr="0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8",
            start_block=start_block,
            latest_block=latest_block,
            block_confirmation=block_confirmation,
            block_range=5,
            event_topic="0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67",
            result_offset=5,
        )

    async def test_end_blocks_greater_than_latest_block(self):
        start_block = 10
        block_range = 6
        block_confirmation = 5
        latest_block = 10

        await concurrent_scan(
            symbols="WETH_USDC",
            max_calls=5,
            pool_addr="0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8",
            start_block=start_block,
            latest_block=latest_block,
            block_confirmation=block_confirmation,
            block_range=block_range,
            event_topic="0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67",
            result_offset=5,
        )
