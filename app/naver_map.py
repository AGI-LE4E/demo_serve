import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

NAVER_MAP_CLIENT_ID = os.getenv("NAVER_MAP_CLIENT_ID")
NAVER_MAP_CLIENT_SECRET = os.getenv("NAVER_MAP_CLIENT_SECRET")


def get_geocode(address: str):
    """Get geocode from address.

    Args:
        address (str): Address to get geocode.
    """
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"

    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_MAP_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVER_MAP_CLIENT_SECRET,
    }

    params = {"query": address}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        result = response.json()
        if result.get("addresses"):
            x = result["addresses"][0].get("x")
            y = result["addresses"][0].get("y")
            return x, y
        else:
            print("No address found.")
            return None, None
    else:
        print(f"Error Code: {response.status_code}")
        return None, None
