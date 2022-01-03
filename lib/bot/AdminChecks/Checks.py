from disnake.ext.commands import check
from disnake import ApplicationCommandInteraction

from lib.db import db


def checkOwner():
    def predicate(ctx: ApplicationCommandInteraction):
        status = db.field("SELECT Status FROM DiscordUser WHERE UserID IS ?", ctx.author.id)
        return True if status == "Owner" else False
    return check(predicate)


def checkAdmin():
    def predicate(ctx: ApplicationCommandInteraction):
        status = db.field("SELECT Status FROM DiscordUser WHERE UserID IS ?", ctx.author.id)
        return True if status == "Admin" else False
    return check(predicate)