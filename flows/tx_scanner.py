import asyncio

from decouple import config
from prefect import task, flow, get_run_logger, get_client
from prefect.task_runners import SequentialTaskRunner

from indexer.scanner import concurrent_scan
from indexer.store import get_max_block_number
from indexer.etherscan import get_latest_block_number

from indexer.utils import hex_to_int

etherscan_rate_limit = int(config("ETHERSCAN_RATE_LIMIT")) or 5

# TODO: BLOCK_CONFIRMATION should configurable in Prefect UI parameter
block_confirmation = int(config("BLOCK_CONFIRMATION")) or 5


# TODO: Get start block of a specific topic of an address instead max block in st
@flow
async def get_start_block(initial_block: int) -> int:
    # Get max block number (max(block)) from store
    max_block = await get_max_block_number()
    if max_block is None:
        max_block = initial_block

    return max_block


@task
async def get_etherscan_rate_limit_config() -> int:
    async with get_client() as client:
        # query the concurrency limit on the 'small_instance' tag
        limit_config = await client.read_concurrency_limit_by_tag(
            tag="etherscan_rate_limit"
        )

    return limit_config.concurrency_limit


@flow(name="tx_scanner", task_runner=SequentialTaskRunner())
async def tx_scanner(
    symbols: str,
    pool_addr: str,
    initial_block: int,
    block_range: int,
    event_topic: str,
    result_offset: int,
):
    logger = get_run_logger()

    # Get start block from store
    start_block = await get_start_block(initial_block)
    logger.info(f"start_block: {start_block}")

    # Get latest block number from Etherscan
    latest_block = hex_to_int(get_latest_block_number())
    logger.info(f"latest_block: {latest_block}")

    # If latest block is in confirmation range, skip and wait for next run
    if latest_block <= start_block + block_confirmation:
        logger.info(f"reach latest block confirmation period, skipping this run")
        return

    rate_limit = await get_etherscan_rate_limit_config()
    if rate_limit is not None:
        etherscan_rate_limit = rate_limit

    # Otherwise, get event logs from Etherscan
    await concurrent_scan(
        symbols=symbols,
        max_calls=etherscan_rate_limit,
        pool_addr=pool_addr,
        start_block=start_block,
        latest_block=latest_block,
        block_confirmation=block_confirmation,
        block_range=block_range,
        event_topic=event_topic,
        result_offset=result_offset,
    )


if __name__ == "__main__":
    asyncio.run(
        tx_scanner(
            symbols="WETH_USDC",
            pool_addr="0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8",
            block_range=2000,
            event_topic="0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67",
            initial_block=12376729,
            result_offset=1000,
        )
    )
