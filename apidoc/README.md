# Project: EVM Transaction Indexer API

## End-point: Get current indexed block

### Method: GET

> ```
> http://127.0.0.1:3001/current_block
> ```

### Response: 200

```json
[
  {
    "max": 17539093
  }
]
```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: Get list of events with pagination

### Method: GET

> ```
> http://127.0.0.1:3001/events?limit=2&offset=0&order=time.desc&time=lte.1687399187&time=gte.1687399187&tx_hash=imatch.0x5aee9b24acb0b7ae1d87bee2be24dfd9d0533d388f879e9f5683e5ba48ce1d30
> ```

### Headers

| Content-Type | Value       |
| ------------ | ----------- |
| Prefer       | count=exact |

### Query Params

| Param   | value                                                                     |
| ------- | ------------------------------------------------------------------------- |
| limit   | 2                                                                         |
| offset  | 0                                                                         |
| order   | time.desc                                                                 |
| time    | lte.1687399187                                                            |
| time    | gte.1687399187                                                            |
| tx_hash | imatch.0x5aee9b24acb0b7ae1d87bee2be24dfd9d0533d388f879e9f5683e5ba48ce1d30 |

### Response: 200

```json
[
  {
    "symbols": "WETH_USDC",
    "time": 1687399187,
    "tx_from": "0x9507c04b10486547584c37bcbd931b2a4fee9a41",
    "tx_to": "0x9507c04b10486547584c37bcbd931b2a4fee9a41",
    "gas": 123561,
    "gas_price": 81774747180,
    "total_fee": null,
    "block": 17532055,
    "value": null,
    "contract_to": "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8",
    "tx_hash": "0x5aee9b24acb0b7ae1d87bee2be24dfd9d0533d388f879e9f5683e5ba48ce1d30"
  }
]
```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃
