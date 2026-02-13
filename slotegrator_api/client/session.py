import asyncio
import hashlib
import hmac
import secrets
import ssl
from http import HTTPMethod, HTTPStatus
from time import time
from urllib.parse import urlencode

import certifi
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from aiohttp.hdrs import USER_AGENT

from slotegrator_api import __version__
from slotegrator_api.exceptions import SlotegratorAPIError
from slotegrator_api.methods import SlotegratorMethod
from slotegrator_api.types import SlotegratorObject


class HTTPSession:
    """HTTP session."""

    def __init__(
        self,
        merchant_id: str,
        merchant_key: str,
        base_api_url: str,
        timeout: float,
    ) -> None:
        self.merchant_id = merchant_id
        self.merchant_key = merchant_key
        self.base_api_url = base_api_url.strip("/")
        self.timeout = timeout
        self._session: ClientSession | None = None
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())

    async def __call__[T: SlotegratorObject](
        self,
        method: SlotegratorMethod[T],
    ) -> T:
        session = await self.create()
        params = method.model_dump(exclude_none=True)
        headers = self.calculate_xsign(
            self.merchant_id,
            self.merchant_key,
            params,
        )
        data = {
            "data"
            if method.__http_method__ == HTTPMethod.POST
            else "params": params,
        }
        async with session.request(
            method.__http_method__,
            method.get_url(self.base_api_url),
            headers=headers,
            **data,
        ) as resp:
            raw_resp = await resp.text()
            if resp.status != HTTPStatus.OK:
                json_resp = await resp.json(content_type=None)
                raise SlotegratorAPIError(
                    method,
                    json_resp["name"],
                    json_resp["message"],
                    json_resp["status"],
                )
            return method.__return_type__.model_validate_json(raw_resp)

    async def create(self) -> ClientSession:
        """Create http session."""
        if self._session is None or self._session.closed:
            self._session = ClientSession(
                timeout=ClientTimeout(self.timeout),
                connector=TCPConnector(
                    ssl_context=self.ssl_context,
                ),
                headers={
                    USER_AGENT: f"slotegratorapi/{__version__}",
                },
            )
        return self._session

    @staticmethod
    def calculate_xsign(
        merchant_id: str,
        merchant_key: str,
        request_params: dict[str, object] | None = None,
    ) -> dict[str, str]:
        """Calculate X-Sign."""
        headers = {
            "X-Merchant-Id": merchant_id,
            "X-Timestamp": str(int(time())),
            "X-Nonce": secrets.token_hex(16),
        }
        merged_params = headers | (request_params or {})
        sorted_params = dict(sorted(merged_params.items()))
        hash_string = urlencode(sorted_params)
        headers |= {
            "X-Sign": hmac.new(
                merchant_key.encode(),
                hash_string.encode(),
                hashlib.sha1,
            ).hexdigest(),
        }
        return headers

    async def close(self) -> None:
        """Close http session."""
        if self._session is not None and not self._session.closed:
            await self._session.close()
            # Wait 250 ms for the underlying SSL connections to close
            await asyncio.sleep(0.25)
