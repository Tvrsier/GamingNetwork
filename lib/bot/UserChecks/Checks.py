from disnake.ext.commands import check
from disnake import ApplicationCommandInteraction

from lib.db import db


class DataError(CommandError):
    def __init__(self):
        super().__init__()


class WRError(CommandError):
    def __init__(self):
        super().__init__()


def checkData():
    def predicate(ctx: ApplicationCommandInteraction):
        allowData = db.field("SELECT ShareData FROM DiscordUser WHERE UserID IS ?", ctx.author.id)
        if allowData != 0:
            return True
        raise DataError
    return check(predicate)


def checkWR():
    def predicate(ctx: ApplicationCommandInteraction):
        exists = db.field("SELECT DiscordID FROM WildRiftUser WHERE DiscordID IS ?", ctx.author.id)
        if exists is not None:
            return True
        raise WRError
    return check(predicate)
