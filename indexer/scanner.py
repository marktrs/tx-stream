import asyncio
import time
import logging

from decouple import config

from etherscan import get_latest_block_number, get_filtered_event_logs
from store import upsert_event_logs, get_max_block_number

initial_block = config("INITIAL_BLOCK") or "1"
block_range = config("BLOCK_RANGE") or "2000"

event_topic = config("EVENT_TOPIC")
event_offset = config("EVENT_OFFSET") or "1000"

pool_addr = config("POOL_CONTRACT")
api_key = config("ETHERSCAN_API_KEY")

polling_period = config("POLLING_PERIOD") or "1"
confirmation_period = config("CONFIRMATION_PERIOD") or "60"

logger = logging.getLogger("indexer-scanner")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


async def get_start_block():
    # Get max block number (max(block)) from store
    max_block = await get_max_block_number()
    if max_block is None:
        max_block = int(initial_block)
    return max_block


async def get_end_block(start_block: int, latest_block: int):
    # Get latest block number from Etherscan
    to_block = start_block + int(block_range)

    # If to_block is greater than latest_block, set to_block to latest_block
    if to_block > latest_block:
        to_block = latest_block


async def scan():
    logger.info("starting scanner for" + pool_addr + "with event topic" + event_topic)

    # Get latest block number from Etherscan
    start_block = await get_start_block()
    latest_block = int(get_latest_block_number(), 16)
    end_block = await get_end_block(start_block, latest_block)

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

    logger.info(
        "start_block: "
        + str(start_block)
        + ", latest_block: "
        + str(latest_block)
        + ", end_block: "
        + str(end_block)
    )

    # If to_block is equal to latest_block, wait for confirmation_period
    if end_block == latest_block:
        time.sleep(confirmation_period)
    else:
        # Else, wait for polling_period to get the next batch of event logs
        time.sleep(polling_period)


while True:
    asyncio.run(scan())
