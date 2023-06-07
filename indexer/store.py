import logging
from decouple import config
from postgrest import AsyncPostgrestClient
from utils import hex_string_to_int, hex_string_to_address


logger = logging.getLogger("indexer-store")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


async def get_max_block_number():
    async with AsyncPostgrestClient(config('POSTGREST_URL')) as client:
        result = await client.from_("ethtxs").select("block").order("block", desc=True).limit(1).execute()
        return result.data[0]['block']


async def upsert_event_logs(result: list):
    async with AsyncPostgrestClient(config('POSTGREST_URL')) as client:
        for r in result:
            logger.info(f"{r['transactionHash']} {r['gasPrice']}")

            await client.from_("ethtxs").upsert({
                "time": hex_string_to_int(r['timeStamp']),
                "txfrom": hex_string_to_address(r['topics'][1]),
                "txto": hex_string_to_address(r['topics'][2]),
                "gas": hex_string_to_int(r['gasUsed']),
                "gasprice": hex_string_to_int(r['gasPrice']),
                "block": hex_string_to_int(r['blockNumber']),
                "txhash": r['transactionHash'],
                "contract_to": "",  # TODO: get contract address
                "contract_value": "",
            }, ignore_duplicates=True, on_conflict="txhash").execute()
