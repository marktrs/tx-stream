import pytest

from unittest import TestCase, skip
from unittest.mock import AsyncMock, Mock
from prefect.testing.utilities import prefect_test_harness

from flows.tx_scan_deployer import (
    create_deployment,
    apply_deployment,
    run_tx_scanner_deployment,
    tx_scan_deployer,
)


@pytest.fixture
def mock_build_from_flow(monkeypatch):
    mock_build_from_flow = AsyncMock()

    # needed to handle `if deployment.storage` check
    ret = Mock()
    ret.storage = None
    mock_build_from_flow.return_value = ret

    monkeypatch.setattr(
        "prefect.cli.deployment.Deployment.build_from_flow", mock_build_from_flow
    )


@pytest.fixture(autouse=True, scope="session")
def prefect_test_fixture():
    with prefect_test_harness():
        yield


@skip("TODO: mock prefect deployment runner")
class TestCreateDeployment(TestCase):
    def test_default(self, mock_build_from_flow):
        create_deployment.fn(symbols="test", interval=10)


class TestApplyDeployment(TestCase):
    def test_default(self):
        apply_deployment.fn(deployment=AsyncMock())


@skip("TODO: mock prefect deployment runner")
class TestRunTxScannerDeployment(TestCase):
    def test_default(self):
        run_tx_scanner_deployment.fn(
            symbols="WETH_USDC",
            pool_addr="0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8",
            initial_block=12376729,
            block_range=2000,
            event_topic="0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67",
            result_offset=1000,
        )


@skip("TODO: mock prefect deployment runner")
class TestTxScanDeployer(TestCase):
    # @patch("flows.tx_scan_deployer.prefect.deployments")
    def test_default(self, run_deployment):
        # run_deployment = MagicMock()
        # run_deployment.return_value = None
        tx_scan_deployer(
            symbols="WETH_USDC",
            pool_addr="0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8",
            initial_block=12376729,
            block_range=2000,
            event_topic="0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67",
            result_offset=1000,
        )
