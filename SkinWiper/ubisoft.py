import asyncio
import aiohttp
import base64
import json

class UbisoftInstance:
    def __init__(self,
                 email: str,
                 password: str,
                 space_id: str = "5172a557-50b5-4665-b7db-e3f2e8c5041d",
                 app_id: str = "39baebad-39e5-4552-8c25-2c9b919064e2"
                 ) -> None:
        self.ticket = ""
        self.session_id = ""
        self.authorised = False

        self.email = email
        self.password = password
        self.user_id = ""
        self.username = ""

        self.space_id = space_id
        self.app_id = app_id

    @property
    def _token(self) -> str:
        return base64.b64encode(f'{self.email}:{self.password}'.encode("utf-8")).decode("utf-8")

    async def login(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method="POST",
                url="https://public-ubiservices.ubi.com/v3/profiles/sessions",
                headers={
                    "Ubi-AppId": self.app_id,
                    "Ubi-RequestedPlatformType": "uplay",
                    "Content-Type": "application/json",
                    "Authorization": f'Basic {self._token}'
                },
                data=json.dumps({"rememberMe": True})
            ) as r:
                data = await r.json()

                if r.status == 200:
                    self.ticket = data['ticket']
                    self.session_id = data['sessionId']
                    self.authorised = True

                    self.user_id = data['userId']
                    self.username = data['nameOnPlatform']
                else:
                    raise InvalidCredentails(json.dumps(data, sort_keys=False, indent=4))

    async def wipe_skins(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method="DELETE",
                url=f"https://public-ubiservices.ubi.com/v1/profiles/{self.user_id}/inventory"
                    f"?spaceId=5172a557-50b5-4665-b7db-e3f2e8c5041d",
                headers={
                    "Ubi-AppId": "39baebad-39e5-4552-8c25-2c9b919064e2",
                    "Authorization": f"Ubi_v1 t={self.ticket}",
                    "Ubi-LocaleCode": "en-gb"
                }
            ) as r:
                data = await r.json()