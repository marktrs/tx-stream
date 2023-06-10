import asyncio
from prefect import flow, get_run_logger
from indexer.scanner import scan


@flow(name="scan_historical_event")
async def scan_historical_event():
    logger = get_run_logger()
    logger.info("starting scanner job")
    await scan()
    logger.info("scanner job completed")


if __name__ == "__main__":
    asyncio.run(scan_historical_event())
