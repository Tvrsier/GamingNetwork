import asyncio
import os
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from disnake import Intents, Guild, Activity, ActivityType, Thread
from disnake.abc import GuildChannel, PrivateChannel
from disnake.ext.commands import *

from .UserChecks.Checks import checkWR_Found, checkWR_NotFound
from ..db import db

prefix = "&"
OWNER_IDS = []
COGS = [path.split("\\")[1][:-3] for path in glob("./lib/cogs/*py")]


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"        {cog} ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class GamingNetwork(Bot):
    def __init__(self):
        self.prefix = prefix
        self.ready = False
        self.token = os.environ["bot_token"]
        self.scheduler = AsyncIOScheduler()
        self.cogs_ready = Ready()
        self.version = ""
        super().__init__(command_prefix=self.prefix, owner_ids=OWNER_IDS, intents=Intents.all())
        db.autosave(self.scheduler)


    def run(self, version):
        self.version = version
        print("Running setup...")
        self.setup()

        print("running bot...")
        super().run(self.token, reconnect=True)

    def setup(self):
        for cog in COGS:
            try:
                print(f"    loadin {cog}")
                self.load_extension(f"lib.cogs.{cog}")
            except NoEntryPointError:
                print(f"    failed to load {cog}\nNo setup found")
            # except ExtensionFailed:
            # print(f"    failed to load {cog}\nThe extension or its setup had an execution error")
            else:
                print(f"    {cog} loaded")

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_guild_join(self, guild: Guild):
        db.execute("INSERT INTO Guild (GuildID, Name, WelcomeMessage) VALUES (?, ?, ?)", guild.id, guild.name, 0)
        db.commit()
        print(f"{guild.name} inserito nella tabella Guild")

    async def on_guild_remove(self, guild: Guild):
        db.execute("DELETE FROM Guild WHERE GuildID IS ?", guild.id)
        db.commit()
        print(f"{guild.name} rimosso dalla tabella Guild")

    async def on_ready(self):
        if not self.ready:
            self.scheduler.start()
            while not self.cogs_ready.all_ready():
                await asyncio.sleep(0.5)
            self.ready = True
            print("Bot ready")
            await self.change_presence(activity=Activity(type=ActivityType.watching, name=f"{len(self.users)} utenti"))

    async def channel_converter(self, channel: int) -> GuildChannel | Thread | PrivateChannel | None:
        """

        :param channel: the ID of the channel
        :return: if exists, the channel object related to its ID
        """
        return self.get_channel(channel)

    async def guild_converter(self, guild: int) -> Guild:
        """

        :param guild: the ID of the guild
        :return: if exists, the guild object related to its ID
        """
        return self.get_guild(guild)


GamingNetwork = GamingNetwork()
