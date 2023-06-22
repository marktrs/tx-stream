from flows.indexer.store import get_max_block_number, upsert_event_logs
from unittest import IsolatedAsyncioTestCase, skip


@skip("TODO: mock postgrest client")
class TestGetMaxBlockNumber(IsolatedAsyncioTestCase):
    async def test_default(
        self,
    ):
        result = await get_max_block_number.fn()
        self.assertIsNotNone(result)
        self.assertIsInstance(result, int)


@skip("TODO: mock postgrest client")
class TestUpsertEventLogs(IsolatedAsyncioTestCase):
    async def test_default(
        self,
    ):
        inputs = {
            "events": [
                {
                    "data": "0x000000000000000000000000000000000000000000000000000000001163871dfffffffffffffffffffffffffffffffffffffffffffffffffdaed63ac6d195350000000000000000000000000000000000005d96c746960387c3da353cb307b40000000000000000000000000000000000000000000000005e0a484c8b12bead00000000000000000000000000000000000000000000000000000000000313db",
                    "topics": [
                        "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67",
                        "0x0000000000000000000000003fc91a3afd70395cd496c647d5a6cc9d4b2b7fad",
                        "0x000000000000000000000000020585f7e9975a0502cf89fcc7d854363779eb22",
                    ],
                    "address": "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8",
                    "gasUsed": "0x43c34",
                    "gasPrice": "0x367088833",
                    "logIndex": "0xeb",
                    "blockHash": "0x30eb21adea4c6e8587b36da26a7681df48b3e6d0fdf78e882411516b9d3a0135",
                    "timeStamp": "0x648924fb",
                    "blockNumber": "0x10aa689",
                    "transactionHash": "0x31650c3a5f1f511ea2bb56ba89a53958308b0f1f5a744db5bc2e3039cc59371c",
                    "transactionIndex": "0x4d",
                }
            ],
            "symbols": "WETH_USDC",
        }

        await upsert_event_logs.fn(
            symbols=inputs["symbols"],
            result=inputs["events"],
        )

    async def test_no_events(
        self,
    ):
        await upsert_event_logs.fn(
            symbols="WETH_USDC",
            events=[],
        )
