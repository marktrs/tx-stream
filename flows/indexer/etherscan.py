import requests

from decouple import config
from prefect import task, get_run_logger

from .event_parser import ResponseParser as parser


@task
def get_latest_block_number() -> str:
    url = (
        f'{config("ETHERSCAN_API_URL")}'
        "module="
        "proxy"
        "&action="
        "eth_blockNumber"
        "&apikey="
        f'{config("ETHERSCAN_API_KEY")}'
    )

    r = requests.get(url, headers={"User-Agent": ""})
    return parser.parse(r)


@task
async def get_filtered_event_logs(
    contract_addr: str,
    from_block: str,
    to_block: str,
    topic: str,
    page: str,
    event_offset: str,
) -> str:
    logger = get_run_logger()
    logger.info(f"topic: {topic}")
    logger.info(f"start_block: {from_block}")
    logger.info(f"to_block: {to_block}")

    url = (
        f'{config("ETHERSCAN_API_URL")}'
        "module="
        "logs"
        "&action="
        "getLogs"
        "&fromBlock="
        f"{from_block}"
        "&toBlock="
        f"{to_block}"
        "&address="
        f"{contract_addr}"
        "&topic0="
        f"{topic}"
        "&page="
        f"{page}"
        "&offset="
        f"{event_offset}"
        "&apikey="
        f'{config("ETHERSCAN_API_KEY")}'
    )

    r = requests.get(url, headers={"User-Agent": ""})
    return parser.parse(r)
