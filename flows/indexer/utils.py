def hex_string_to_address(hex_string: str):
    """Converts a hex string to an address."""
    hex_string = hex_string.replace("0x", "")
    hex_string = hex_string.lstrip("0")
    shortened_hex = "0x" + hex_string
    return shortened_hex


def hex_string_to_int(hex_string: str):
    """Converts a hex string to an integer."""
    if len(hex_string) <= 2:
        # gasPrice can be "0x",
        return 0
    elif hex_string[:2] == "0x":
        hex_string = hex_string[2:]
    return int(hex_string, 16)
