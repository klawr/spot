import asyncio
import discord
import json as json

from os.path import exists

class Spot(discord.Client):
    """
    import spot
    with spot('./config.json') as spot:
        spot.message('i love you')
    """

    def __init__(
        self,
        file=None,
        id=None,
        token=None,
        loop=asyncio.new_event_loop(),
        *args,
        **kwargs
    ):

        if file is not None and exists(file):
            with open(file) as config:
                auth = json.load(config)
                id = auth["id"]
                token = auth["token"]
        elif id is None and token is None:
            print("spot can not authenticate.")
            return
        else:
            print("spot file not found at " + file)
            return

        self.loop = loop
        super().__init__(*args, **kwargs)

        async def login(token):
            await self.login(token)
            user = await self.fetch_user(id)
            self.channel = await user.create_dm()

        self.loop.run_until_complete(login(token))

    def __enter__(self):
        return self

    def exit(self):
        async def goodbye():
            await self.close()

        self.loop.run_until_complete(goodbye())

    def __exit__(self, *args):
        self.exit()

    def message(self, text):
        if (self.loop):
            self.loop.run_until_complete(self.channel.send(text))
