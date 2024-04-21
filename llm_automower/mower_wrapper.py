"""
Much of this code is based on https://github.com/Thomas55555/aioautomower/blob/main/src/aioautomower/example.py
"""
from typing import cast
import time

from aiohttp import ClientSession

from aioautomower.auth import AbstractAuth
from aioautomower.const import API_BASE_URL
from aioautomower.session import AutomowerSession
from aioautomower.utils import (
    async_get_access_token,
    convert_timestamp_to_datetime_utc,
    structure_token,
)

CLOCK_OUT_OF_SYNC_MAX_SEC = 20

class AsyncTokenAuth(AbstractAuth):
    """Provide Automower authentication tied to an OAuth2 based config entry."""

    def __init__(self, websession: ClientSession, base_url:str, client_id:str, client_secret:str) -> None:
        """Initialize Husqvarna Automower auth."""
        super().__init__(websession, base_url)
        self.token: dict = {}
        self.client_id = client_id
        self.client_secret = client_secret

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        if not self.token:
            self.token = await async_get_access_token(self.client_id, self.client_secret)
            _ = structure_token(self.token["access_token"])
        return self.token["access_token"]

    @property
    def valid_token(self) -> bool:
        """Return if token is still valid."""
        return (
            cast(float, self.token["expires_at"])
            > time.time() + CLOCK_OUT_OF_SYNC_MAX_SEC
        )

    async def async_ensure_token_valid(self) -> None:
        """Ensure that the current token is valid."""
        if self.valid_token:
            return
        self.token = await async_get_access_token(self.client_id, self.client_secret)

class MowerWrapper():

    def __init__(self, client_id: str, client_secret:str, mower_id: str = None):
        websession = ClientSession()
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth = AsyncTokenAuth(websession, API_BASE_URL, self.client_id, self.client_secret)
        self.api = AutomowerSession(self.auth, poll=True)
        self.mower_id = mower_id

    async def connect(self):
        """Connect to the API and return the status of the mower."""
        await self.api.connect()
        status = await self.api.get_status()

        if self.mower_id is None:
            mowers = list(status.keys())
            if len(mowers) > 0:
                self.mower_id = mowers[0]
            else:
                raise ValueError("No mowers found in API")
        else:
            if self.mower_id not in status:
                raise ValueError(f"Mower {self.mower_id} not found in API")

        return status[self.mower_id], self.mower_id

    async def set_calendar(self, tasks_list):
        """Set the calendar of the mower."""
        return await self.api.set_calendar(self.mower_id, tasks_list)