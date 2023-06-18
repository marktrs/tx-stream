import requests

from decouple import config
from prefect import task, get_run_logger

from .event_parser import parse


# TODO: Configurable in Prefect UI parameter to be able to run on different network/ topic
api_url = config("ETHERSCAN_API_URL")
# TODO: Configurable in Prefect UI parameter to be able to run on different network/ topic
api_key = config("ETHERSCAN_API_KEY")


@task
def get_latest_block_number() -> str:
    url = (
        f"{api_url}"
        "module="
        "proxy"
        "&action="
        "eth_blockNumber"
        "&apikey="
        f"{api_key}"
    )

    r = requests.get(url, headers={"User-Agent": ""})
    return parse(r)


@task
async def get_filtered_event_logs(
    contract_addr: str,
    topic: str,
    from_block: int,
    to_block: int,
    page: int,
    result_offset: int,
) -> str:
    url = (
        f"{api_url}"
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
        f"{result_offset}"
        "&apikey="
        f"{api_key}"
    )

    r = requests.get(url, headers={"User-Agent": ""})

    return parse(r)
