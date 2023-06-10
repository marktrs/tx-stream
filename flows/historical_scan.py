import asyncio

from decouple import config
from prefect import flow, get_run_logger
from prefect.task_runners import SequentialTaskRunner

from indexer.scanner import concurrent_scan
from indexer.store import get_max_block_number
from indexer.etherscan import get_latest_block_number

# TODO: INITIAL_BLOCK, should configurable in Prefect UI parameter
initial_block = config("INITIAL_BLOCK") or "1"
block_range = config("BLOCK_RANGE") or "2000"

# TODO: Get event topic from ABI, Topic should be configurable in Prefect UI parameter
event_topic = config("EVENT_TOPIC")
event_offset = config("EVENT_OFFSET") or "1000"

# TODO: Get contract from ABI to decode topic, POOL contract should configurable in Prefect UI parameter
pool_addr = config("POOL_CONTRACT")

# TODO: Configurable in Prefect UI parameter to be able to run on different network/ topic
api_key = config("ETHERSCAN_API_KEY")

# TODO: CONFIRMATION_BLOCKS should configurable in Prefect UI parameter
confirmation_blocks = config("CONFIRMATION_BLOCKS") or "10"

# TODO: 'API rate limit' should configurable in Prefect UI parameter
etherscan_rate_limit = config("ETHERSCAN_RATE_LIMIT") or "5"


# TODO: Get start block for a specific topic of an address
@flow
async def get_start_block() -> int:
    # Get max block number (max(block)) from store
    max_block = await get_max_block_number()
    if max_block is None:
        max_block = int(initial_block)

    return max_block


async def get_end_block(start_block: int, latest_block: int) -> int:
    # Get latest block number from Etherscan
    to_block = start_block + int(block_range)

    # If to_block is greater than latest_block, set to_block to latest_block
    if to_block > latest_block:
        to_block = latest_block

    return to_block


@flow(name="scan_historical_event", task_runner=SequentialTaskRunner())
async def scan_historical_event():
    logger = get_run_logger()

    # Get start block from store
    start_block = await get_start_block()
    logger.info(f"start_block: {start_block}")

    # Get latest block number from Etherscan
    latest_block = int(get_latest_block_number(), 16)
    logger.info(f"latest_block: {latest_block}")

    # If latest block is in confirmation range, skip and wait for next run
    if int(latest_block) <= int(start_block) + int(confirmation_blocks):
        logger.info(f"reach latest block confirmation period, skipping this run")
        return

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
    asyncio.run(scan_historical_event())
