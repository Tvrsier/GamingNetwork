import sys
import traceback
from disnake.ext.commands import *
from disnake import ApplicationCommandInteraction, Member

from ..db import db
from lib.bot.AdminChecks.Checks import checkOwner


class Admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="pex", description="Gives administrator permissions to an user",
                   guild_ids=[865691556736008213])
    @checkOwner()
    async def pex(self, ctx: ApplicationCommandInteraction, user: Member):
        status = db.field("SELECT Status FROM DiscordUser WHERE UserID IS ?", user.id)
        if status != "Admin":
            db.execute("UPDATE DiscordUser SET Status = ? WHERE UserID IS ?", "Admin", user.id)
            db.commit()
            await ctx.send(f"{user.name} è ora un Amministratore di GamingNetwork", ephemeral=True)

    @slash_command(name="depex", description="Removes administrator permissions to an user",
                   guild_ids=[865691556736008213])
    @checkOwner()
    async def depex(self, ctx: ApplicationCommandInteraction, user: Member):
        status = db.field("SELECT Status From DiscordUser WHERE UserID IS ?", user.id)
        if status == "Admin":
            db.execute("UPDATE DiscordUser SET Status = ? WHERE UserID IS ?", "User", user.id)
            db.commit()
            await ctx.send(f"{user.name} non è più un Amministratore di GamingNetwork", ephemeral=True)

    @pex.error
    async def pex_error(self, ctx: ApplicationCommandInteraction, error: CommandError):
        if isinstance(error, CheckFailure):
            await ctx.send("Non possiedi i permessi per eseguire questo comando", ephemeral=True)
            return
        else:
            await ctx.send("Qualcosa è andato storto.\nSe sei un admin controlla la console")
            print(f"Ignoring exception in command {ctx.application_command}", file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @depex.error
    async def depex_error(self, ctx: ApplicationCommandInteraction, error: CommandError):
        if isinstance(error, CheckFailure):
            await ctx.send("Non possiedi i permessi per eseguire questo comando", ephemeral=True)
            return
        else:
            await ctx.send("Qualcosa è andato storto.\nSe sei un admin controlla la console", ephemeral=True)
            print(f"Ignoring exception in command {ctx.application_command}", file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("admin")


def setup(bot):
    bot.add_cog(Admin(bot))