import requests


def parse(response: requests.Response):
    content = response.json()
    result = content["result"]

    if "status" in content.keys():
        message = "no message provided"
        status = bool(int(content["status"]))
        if "status" in content.keys():
            message = content["message"]
        assert status, f"{result} -- {message}"
    else:
        # GETH or Parity proxy msg format
        # TODO: see if we need those values
        jsonrpc = content["jsonrpc"]
        cid = int(content["id"])

    return result
