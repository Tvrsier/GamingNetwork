import sys
import traceback

from disnake import ApplicationCommandInteraction
from disnake.ext.commands import *

from lib.bot.UserChecks.Checks import DataError, WRError


class errorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context | ApplicationCommandInteraction, error: CommandError):
        if isinstance(error, MissingPermissions):
            if isinstance(ctx, ApplicationCommandInteraction):
                await ctx.send("Non hai i permessi per utilizzare questo comando", ephemeral=True)
                return
            await ctx.send("Non hai i permessi per utilizzare questo comando", delete_after=7)
        elif isinstance(error, DataError):
            if isinstance(ctx, ApplicationCommandInteraction):
                await ctx.send("Questo comando richiede il consenso al trattamento dei dati, digita /allow_save_data se"
                               " desideri dare il consenso", ephemeral=True)
                return
            await ctx.send("Non hai i permessi per utilizzare questo comando", delete_after=7)
        elif isinstance(error, WRError):
            if isinstance(ctx, ApplicationCommandInteraction):
                if ctx.data.name == "register":
                    await ctx.send("Sei già registrato", ephemeral=True)
                await ctx.send("Per utilizzare questo comando hai bisogno di registrare i tuoi dati di Wild Rift",
                               ephemeral=True)
                await ctx.send("Per utilizzare questo comando hai bisogno di registrare i tuoi dati di Wild Rift",
                               ephemeral=True)
        else:
            print(f"ignoring exception in command", file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @Cog.listener()
    async def on_slash_command_error(self, ctx: Context | ApplicationCommandInteraction, error: CommandError):
        if isinstance(error, MissingPermissions):
            if isinstance(ctx, ApplicationCommandInteraction):
                await ctx.send("Non hai i permessi per utilizzare questo comando", ephemeral=True)
                return
            await ctx.send("Non hai i permessi per utilizzare questo comando", delete_after=7)
        elif isinstance(error, DataError):
            if isinstance(ctx, ApplicationCommandInteraction):
                await ctx.send("Questo comando richiede il consenso al trattamento dei dati, digita /allow_save_data se"
                               " desideri dare il consenso", ephemeral=True)
                return
            await ctx.send("Non hai i permessi per utilizzare questo comando", delete_after=7)
        elif isinstance(error, WRError):
            if isinstance(ctx, ApplicationCommandInteraction):
                if ctx.data.name == "register":
                    await ctx.send("Sei già registrato", ephemeral=True)
                    return
                await ctx.send("Per utilizzare questo comando hai bisogno di registrare i tuoi dati di Wild Rift",
                               ephemeral=True)
                return
        else:
            print(f"ignoring exception in command", file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("ErrorHandler")


def setup(bot):
    bot.add_cog(errorHandler(bot))