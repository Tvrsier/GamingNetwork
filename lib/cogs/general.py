from disnake.ext.commands import *
from disnake import Embed, ApplicationCommandInteraction

from datetime import datetime
from ..db import db
from ..bot.askData import askData

class General(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="allow_save_data", description="Permetti al bot di salvare i tuoi dati",
                   guild_ids=[865691556736008213])
    async def allow_save_data(self, ctx: ApplicationCommandInteraction):
        share_data = db.field("SELECT ShareData FROM DiscordUser WHERE UserID IS ?", ctx.author.id)
        if share_data == 0 or share_data == None:
            await askData(ctx, ctx.author)
        else:
            await ctx.send("Hai già dato il consenso", ephemeral=True)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("general")


def setup(bot):
    bot.add_cog(General(bot))
