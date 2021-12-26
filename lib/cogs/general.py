from disnake.ext.commands import *
from disnake import Embed, ApplicationCommandInteraction, Guild, User

from datetime import datetime
from ..db import db
from ..bot.askData import *
class General(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="allow_save_data", description="Permetti al bot di salvare i tuoi dati",
                   guild_ids=[865691556736008213])
    async def allow_save_data(self, ctx: ApplicationCommandInteraction):
        # Improved askData
        user = db.record("SELECT * FROM DiscordUser WHERE UserID IS ?", ctx.author.id)
        if user is not None:
            if user[-1] == 0 or user[-1] is None:
                await askData(ctx, ctx.author)
            else:
                await ctx.send("Hai già dato il consenso", ephemeral=True)
        else:
            await askDataToNewMember(ctx.author, ctx)

    @Cog.listener()
    async def on_guild_update(self, before: Guild, after: Guild):
        if before.name != after.name:
            db.execute("UPDATE Guild SET Name = ? WHERE GuildID IS ?", after.name, after.id)
            db.commit()

    @Cog.listener()
    async def on_user_update(self, before: User, after: User):
        exists = db.field("SELECT UserID FROM DiscordUser WHERE UserID IS ?", after.id)
        if exists:
            if before.name != after.name:
                db.execute("UPDATE DiscordUser SET UserName = ? Where UserID IS ?", after.name, after.id)
                db.commit()
            if before.discriminator != after.discriminator:
                db.execute("UPDATE DiscordUser SET Discriminator = ? Where UserID IS ?", after.discriminator, after.id)
                db.commit()

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("general")


def setup(bot):
    bot.add_cog(General(bot))
