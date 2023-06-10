import asyncio

from decouple import config
from prefect import flow, get_run_logger, get_client
from prefect.task_runners import SequentialTaskRunner

from indexer.scanner import concurrent_scan
from indexer.store import get_max_block_number
from indexer.etherscan import get_latest_block_number

from indexer.utils import hex_to_int

# Shared config between symbol

# TODO: CONFIRMATION_BLOCKS should configurable in Prefect UI parameter
confirmation_blocks = int(config("CONFIRMATION_BLOCKS")) or 5
etherscan_rate_limit = int(config("ETHERSCAN_RATE_LIMIT")) or 5

# Shared config within contract
# TODO: Get contract from ABI to decode topic, POOL contract should configurable in Prefect UI parameter
pool_addr = config("POOL_CONTRACT")
# TODO: INITIAL_BLOCK should configurable in Prefect UI parameter
initial_block = int(config("INITIAL_BLOCK")) or 1
# TODO: block_range should configurable in Prefect UI parameter
block_range = int(config("BLOCK_RANGE")) or 2000

# Shared config within topic
# TODO: Get event topic from ABI, Topic should be configurable in Prefect UI parameter
event_topic = config("EVENT_TOPIC")
# TODO: EVENT_OFFSET, Topic should be configurable in Prefect UI parameter
event_offset = config("EVENT_OFFSET") or 1000


# TODO: Get start block of a specific topic of an address instead max block in st
@flow
async def get_start_block() -> int:
    # Get max block number (max(block)) from store
    max_block = await get_max_block_number()
    if max_block is None:
        max_block = initial_block

    return max_block


async def get_end_block(start_block: int, latest_block: int) -> int:
    # Get latest block number from Etherscan
    to_block = start_block + block_range

    # If to_block is greater than latest_block, set to_block to latest_block
    if to_block > latest_block:
        to_block = latest_block

    return to_block


async def get_etherscan_rate_limit_config() -> int:
    async with get_client() as client:
        # query the concurrency limit on the 'small_instance' tag
        limit_config = await client.read_concurrency_limit_by_tag(
            tag="etherscan_rate_limit"
        )

    return limit_config.concurrency_limit


@flow(name="scan_event_history", task_runner=SequentialTaskRunner())
async def scan_event_history():
    logger = get_run_logger()

    # Get start block from store
    start_block = await get_start_block()
    logger.info(f"start_block: {start_block}")

    # Get latest block number from Etherscan
    latest_block = hex_to_int(get_latest_block_number())
    logger.info(f"latest_block: {latest_block}")

    # If latest block is in confirmation range, skip and wait for next run
    if latest_block <= start_block + confirmation_blocks:
        logger.info(f"reach latest block confirmation period, skipping this run")
        return

    rate_limit = await get_etherscan_rate_limit_config()
    if rate_limit is not None:
        etherscan_rate_limit = rate_limit

    # Otherwise, get event logs from Etherscan
    await concurrent_scan(
        max_calls=etherscan_rate_limit,
        pool_addr=pool_addr,
        start_block=start_block,
        latest_block=latest_block,
        confirmation_blocks=confirmation_blocks,
        block_range=block_range,
        event_topic=event_topic,
        event_offset=event_offset,
    )


if __name__ == "__main__":
    asyncio.run(scan_event_history())
