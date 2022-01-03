from disnake.ext.commands import *
from lib.bot.UserChecks.Checks import checkData
from lib.bot.askData import *
from lib.Games.WildRift.User import User

picklePath = "./data/pickle/WR"


class WildRift(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("WildRift")


def setup(bot):
    bot.add_cog(WildRift(bot))