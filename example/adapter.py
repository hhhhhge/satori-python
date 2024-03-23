import asyncio
from datetime import datetime
from typing import Any

from launart import Launart

from satori import Channel, ChannelType, Event, Text, User
from satori.model import Login, LoginStatus, MessageObject
from satori.server import Adapter, Request


class ExampleAdapter(Adapter):
    @property
    def required(self):
        return set()

    @property
    def stages(self):
        return {"blocking"}

    def get_platform(self) -> str:
        return "example"

    def validate_headers(self, headers: dict) -> bool:
        return headers["X-Platform"] == self.get_platform()

    def authenticate(self, token: str) -> bool:
        return True

    async def get_logins(self):
        return [Login(LoginStatus.ONLINE, self_id="1234567890", platform="example")]

    async def call_api(self, req: Request) -> Any:
        print(req)  # noqa: T201
        return MessageObject.from_elements("1234", [Text("example")]).dump()

    async def call_internal_api(self, request: Request[dict]) -> Any:
        return "example"

    async def publisher(self):
        seq = 0
        while True:
            await asyncio.sleep(2)
            yield Event(
                seq,
                "message-created",
                self.get_platform(),
                "1234567890",
                datetime.now(),
                channel=Channel("345678", ChannelType.TEXT),
                user=User("9876543210"),
                message=MessageObject(f"msg_{seq}", "test"),
            )
            seq += 1

    async def launch(self, manager: Launart):
        async with self.stage("blocking"):
            await manager.status.wait_for_sigexit()
