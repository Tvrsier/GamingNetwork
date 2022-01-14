from disnake import ApplicationCommandInteraction
from disnake.ext.commands import check, CheckFailure

from lib.db import db


class DataError(CheckFailure):
    def __init__(self):
        super().__init__()


class WRError(CheckFailure):
    def __init__(self):
        super().__init__(message="This user cannot use this command because he doesn't satisfy the necessary "
                                 "requirements")


def checkData():
    def predicate(ctx: ApplicationCommandInteraction):
        allowData = db.field("SELECT ShareData FROM DiscordUser WHERE UserID IS ?", ctx.author.id)
        if allowData != 0:
            return True
        raise DataError()

    return check(predicate)


def checkWR_Found():
    def predicate(ctx: ApplicationCommandInteraction):
        exists = db.field("SELECT DiscordID FROM WildRiftUser WHERE DiscordID IS ?", ctx.author.id)
        if exists is not None:
            return True
        raise WRError()

    return check(predicate)


def checkWR_NotFound():
    def predicate(ctx: ApplicationCommandInteraction):
        not_exist = db.field("SELECT DiscordID FROM WildRiftUser WHERE DiscordID IS ?", ctx.author.id)
        if not_exist is None:
            return True
        raise WRError

    return check(predicate)
