import pytest

from unittest import IsolatedAsyncioTestCase, skip
from prefect.testing.utilities import prefect_test_harness
from flows.tx_scanner import tx_scanner
from prefect.client import get_client


@pytest.fixture(autouse=True, scope="session")
def prefect_test_fixture():
    with prefect_test_harness():
        yield


@skip("TODO: mock prefect client")
class TestTxScanner(IsolatedAsyncioTestCase):
    def test_default(self):
        tx_scanner(
            symbols="WETH_USDC",
            pool_addr="0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8",
            block_range=2000,
            event_topic="0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67",
            initial_block=12376729,
            result_offset=1000,
        )
