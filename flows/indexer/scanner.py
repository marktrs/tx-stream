import time
import asyncio

from prefect import flow, get_run_logger
from decouple import config
from .store import upsert_event_logs, get_max_block_number
from .etherscan import get_latest_block_number, get_filtered_event_logs

initial_block = config("INITIAL_BLOCK") or "1"
block_range = config("BLOCK_RANGE") or "2000"

event_topic = config("EVENT_TOPIC")
event_offset = config("EVENT_OFFSET") or "1000"

pool_addr = config("POOL_CONTRACT")
api_key = config("ETHERSCAN_API_KEY")

polling_period = config("POLLING_PERIOD") or "1"
confirmation_blocks = config("CONFIRMATION_BLOCKS") or "10"


@flow
async def get_start_block() -> int:
    # Get max block number (max(block)) from store
    max_block = await get_max_block_number()
    if max_block is None:
        max_block = int(initial_block)

    return max_block


@flow
async def get_end_block(start_block: int, latest_block: int) -> int:
    # Get latest block number from Etherscan
    to_block = start_block + int(block_range)

    # If to_block is greater than latest_block, set to_block to latest_block
    if to_block > latest_block:
        to_block = latest_block

    return to_block


@flow
async def scan():
    logger = get_run_logger()
    # Get latest block number from Etherscan
    start_block = await get_start_block()
    logger.info(f"start_block: {start_block}")

    latest_block = int(get_latest_block_number(), 16)
    logger.info(f"latest_block: {latest_block}")

    end_block = await get_end_block(start_block, latest_block)
    logger.info(f"end_block: {end_block}")

    # If latest block is in confirmation range, skip and wait for next run
    if int(latest_block) < int(end_block) + 60:
        logger.info(f"reach latest block, sleeping for {confirmation_blocks} seconds")
        return

    # With proper block range and offset=1000, we usually get all events in one page
    # TODO: Handle pagination if result exceeds 1000
    page = "1"

    # Get filtered event logs from Etherscan
    events = get_filtered_event_logs(
        contract_addr=pool_addr,
        from_block=start_block,
        to_block=end_block,
        page=page,
        topic=event_topic,
        event_offset=event_offset,
    )

    # TODO: Decode event logs data to human readable format and properly store them
    # data = decode_event_logs(events)

    # Add batch of filtered event logs to store
    await upsert_event_logs(events)
