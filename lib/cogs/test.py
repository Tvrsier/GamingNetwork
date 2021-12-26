from disnake.ext.commands import *
from disnake import Embed, ApplicationCommandInteraction, Member

from datetime import datetime
from ..db import db
from lib.bot.askData import askDataToNewMember


class Test(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Bot speed test")
    async def ping(self, ctx: ApplicationCommandInteraction):
        embed = Embed(title="Bot latency:", timestamp=datetime.utcnow())
        embed.add_field(name=f":clock1:PONG! {round(self.bot.latency * 1000)}ms", value="\u00AD")
        await ctx.send(embed=embed)
        print(f"{ctx.author.id}")
        user_converter = UserConverter()
        ctx_converter = await self.bot.get_context(await ctx.original_message())
        user = await user_converter.convert(ctx_converter, str(ctx.author.id))
        print(f"{user}, {ctx.author}")

    @slash_command(description="Di qualcosa")
    async def echo(self, ctx: ApplicationCommandInteraction,
                   message: str = Param(description="Il messaggio da inviare")):
        embed = Embed(title="\u00AD", timestamp=datetime.utcnow())
        embed.add_field(name=f"{ctx.author.name} ha detto: {message}", value="\u00AD", inline=False)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_member_join(self, user: Member):
        # Improved askData
        is_recorded = db.record("SELECT * FROM DiscordUser WHERE UserID IS ?", user.id)
        if not is_recorded:
            await askDataToNewMember(user)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("test")


def setup(bot):
    bot.add_cog(Test(bot))
