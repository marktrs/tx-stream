from prefect import flow

from decouple import config
from postgrest import AsyncPostgrestClient

from .utils import hex_string_to_int, hex_string_to_address


@flow
async def get_max_block_number():
    async with AsyncPostgrestClient(config("POSTGREST_URL")) as client:
        result = (
            await client.from_("events")
            .select("block")
            .order("block", desc=True)
            .limit(1)
            .execute()
        )

        if len(result.data) == 0:
            return None

        return result.data[0]["block"]


@flow
async def upsert_event_logs(result: list):
    async with AsyncPostgrestClient(config("POSTGREST_URL")) as client:
        for r in result:
            await client.from_("events").upsert(
                {
                    "time": hex_string_to_int(r["timeStamp"]),
                    "tx_from": hex_string_to_address(r["topics"][1]),
                    "tx_to": hex_string_to_address(r["topics"][2]),
                    "gas": hex_string_to_int(r["gasUsed"]),
                    "gas_price": hex_string_to_int(r["gasPrice"]),
                    "block": hex_string_to_int(r["blockNumber"]),
                    "tx_hash": r["transactionHash"],
                    "contract_to": hex_string_to_address(
                        r["address"]
                    ),  # TODO: get contract address
                    # "contract_value": "",
                },
                ignore_duplicates=True,
                on_conflict="tx_hash",
            ).execute()
