from prefect import flow

from decouple import config
from postgrest import AsyncPostgrestClient

from .utils import hex_to_int, hex_to_address


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
async def upsert_event_logs(symbols: str, result: list):
    data = [
        {
            "symbols": symbols,
            "time": hex_to_int(r["timeStamp"]),
            "tx_from": hex_to_address(r["topics"][1]),
            "tx_to": hex_to_address(r["topics"][2]),
            "gas": hex_to_int(r["gasUsed"]),
            "gas_price": hex_to_int(r["gasPrice"]),
            "block": hex_to_int(r["blockNumber"]),
            "tx_hash": r["transactionHash"],
            "contract_to": hex_to_address(r["address"]),
            # "contract_value": "", TODO: Decode event log value
        }
        for r in result
        if r is not None
    ]
    async with AsyncPostgrestClient(config("POSTGREST_URL")) as client:
        await client.from_("events").upsert(
            data,
            ignore_duplicates=True,
            on_conflict="tx_hash",
        ).execute()
