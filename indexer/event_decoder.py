import json
from web3 import Web3

# TODO: Add more event decoders


def decode_transaction_event_log(input_string):
    input_bytes = bytes.fromhex(input_string[2:])
    decoded_data = Web3.codec.decode_abi(
        ['int', 'uint', 'uint', 'uint', 'int'], input_bytes)

    decoded_dict = {
        "amount0": decoded_data[0],
        "amount1": decoded_data[1],
        "sqrtPriceX96": decoded_data[2],
        "liquidity": decoded_data[3],
        "tick": decoded_data[4]
    }

    return json.dumps(decoded_dict, indent=2)
