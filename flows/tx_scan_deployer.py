import tx_scanner as scanner

from prefect import flow
from prefect.deployments import Deployment, run_deployment
from prefect.server.schemas.schedules import IntervalSchedule


@flow
def create_deployment(symbols: str, interval: int):
    return Deployment.build_from_flow(
        flow=scanner.tx_scanner,
        name=symbols,
        version=1,
        work_pool_name="default-agent-pool",
        schedule=(IntervalSchedule(interval=interval)),
    )


@flow
def apply_deployment(deployment):
    deployment.apply()


@flow
def run_tx_scanner_deployment(
    symbols: str,
    pool_addr: str,
    initial_block: int,
    block_range: int,
    event_topic: str,
    result_offset: int,
):
    run_deployment(
        name=f"tx_scanner/{symbols}",
        flow_run_name="tx_scanner",
        parameters={
            "pool_addr": pool_addr,
            "initial_block": initial_block,
            "block_range": block_range,
            "event_topic": event_topic,
            "result_offset": result_offset,
        },
    )


@flow(name="tx_scan_deployer")
def tx_scan_deployer(
    symbols: str,
    pool_addr: str,
    event_topic: str,
    result_offset: int,
    block_range: int = 2000,
    initial_block: int = 1,
    polling_interval_sec: int = 10,
):
    deployment = create_deployment(symbols, interval=polling_interval_sec)
    apply_deployment(deployment)
    run_tx_scanner_deployment(
        symbols=symbols,
        pool_addr=pool_addr,
        initial_block=initial_block,
        block_range=block_range,
        event_topic=event_topic,
        result_offset=result_offset,
    )


if __name__ == "__main__":
    # default to WETH_USDC when running locally
    tx_scan_deployer(
        symbols="WETH_USDC",
        polling_interval_sec=10,
        pool_addr="0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8",
        initial_block=12376729,
        block_range=2000,
        event_topic="0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67",
        result_offset=1000,
    )
