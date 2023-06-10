def hex_to_address(hex: str):
    """Converts a hex string to an address."""
    hex = hex.replace("0x", "")
    hex = hex.lstrip("0")
    return "0x" + hex


def hex_to_int(hex: str):
    """Converts a hex string to an integer."""
    if len(hex) <= 2:
        # gasPrice can be "0x",
        return 0
    elif hex[:2] == "0x":
        hex = hex[2:]
    return int(hex, 16)
