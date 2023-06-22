import asyncio

from prefect import flow
from .store import upsert_event_logs
from .etherscan import get_filtered_event_logs


@flow
async def concurrent_scan(
    symbols: str,
    max_calls: int,
    latest_block: int,
    start_block: int,
    block_confirmation: int,
    block_range: int,
    pool_addr: str,
    event_topic: str,
    result_offset: int,
):
    # With proper block range and offset=1000, we usually get all events in one page
    # TODO: Handle pagination if result exceeds 1000
    page = "1"

    calls = []

    last_scanned_block = start_block + block_range * 5

    for _ in range(max_calls):
        if latest_block <= start_block + block_confirmation:
            # reached latest block, stop scanning
            break

        end_block = start_block + block_range

        if end_block > latest_block:
            end_block = latest_block - block_confirmation
            last_scanned_block = end_block

        call = get_filtered_event_logs(
            contract_addr=pool_addr,
            from_block=start_block,
            to_block=end_block,
            page=page,
            topic=event_topic,
            result_offset=result_offset,
        )

        calls.append(call)
        start_block = end_block + 1

    if len(calls) == 0:
        return

    results = await asyncio.gather(*calls)

    events = []
    for result in results:
        if len(result) == result_offset:
            raise ValueError(
                f"Found {len(result)} events in block range {start_block} to {last_scanned_block}, current offset is {result_offset} please increase RESULT_OFFSET and re-run this flow"
            )
        if result is not None:
            events.extend(result)

    # TODO: Decode event logs data to human readable format and properly store them
    # data = decode_event_logs(events)

    # Add batch of filtered event logs to store
    await upsert_event_logs(symbols, events)
