import sys
from typing import Dict

from dotenv import load_dotenv
import os
import hmac
import hashlib
from urllib.parse import urlencode
import requests


class EdFestCli:

    base_url = "https://api.edinburghfestivalcity.com"

    def __init__(self):
        load_dotenv()
        self._apikey = os.getenv("api_key")
        self._apisecret = os.getenv("api_secret")

    def events(self, params: Dict) -> Dict:
        return self._send_request("events", params)

    def venues(self, params: Dict):
        return self._send_request("venues", params)

    def _send_request(self, path: str, params: Dict) -> Dict:
        params["key"] = self._apikey
        query = urlencode(params)
        url_to_sign = f"/{path}?{query}"
        signature = hmac.new(
            self._apisecret.encode("utf-8"), url_to_sign.encode("utf-8"), hashlib.sha1
        ).hexdigest()
        signed_url = f"{url_to_sign}&signature={signature}"
        url_to_request = f"{EdFestCli.base_url}{signed_url}"
        original_stderr = sys.stderr  # Save the original stderr
        with open("error.log", "a") as f:
            sys.stderr = f  # Redirect stderr to the file

            # Any stderr output now goes to 'error.log'
            print(url_to_request, file=sys.stderr)
        sys.stderr = original_stderr  # Restore the original stderr
        response = requests.get(url_to_request)
        return response.json()
