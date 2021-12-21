from lib.db import db
from lib.bot import GamingNetwork
from disnake import Member, DMChannel, ApplicationCommandInteraction
import asyncio


async def askDataToJoinedMember(user: Member):
    channel: DMChannel = await user.create_dm()
    message = await channel.send(f"Ciao {user.name}\nIo sono GamingNetwork, un bot che vuole aiutare voi "
                                 f"utenti a trovare altre persone con cui giocare!\nDevo avvertirti che "
                                 f"per funzionare utilizzo alcuni tuoi dati di discord e dei tuoi giochi, "
                                 f"per tanto mi serve il tuo consenso a collezionarli!\n"
                                 f"Rispondi semplicemente con \"Si\" o \"No\"\n"
                                 f"N.B: Se la risposta fosse negativa, questa domanda ti verrà posta ogni "
                                 f"volta che proverai ad usare dei comandi che richiedono i tuoi dati, "
                                 f"Senza il consenso questi comandi non potranno essere usati")
    check = lambda m: m.author == user and m.channel == channel
    try:
        confirm = await GamingNetwork.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await message.edit(content="Ci hai impiegato troppo a inviarmi una risposta :pensive:")
        return
    if confirm.content.lower() == "si":
        await message.edit(content="Hai dato il consenso! procedo con il salvataggio")
        db.execute("INSERT INTO DiscordUser (UserID, Discriminator, UserName, ShareData) "
                   "VALUES (?, ?, ?, ?)", user.id, user.discriminator, user.name, 1)
        db.commit()
        return
    elif confirm.content.lower() == "no":
        await message.edit(content="Ci dispiace di non essere degni della tua fiducia :pensive:")
        db.execute("INSERT INTO DiscordUser (UserID, Discriminator, UserName, ShareData) "
                   "VALUES (?, ?, ?, ?)", user.id, user.discriminator, user.name, 0)
        db.commit()
        return
    else:
        await message.edit(content="Non riesco ad analizzare la tua risposta :pensive:")
        db.execute("INSERT INTO DiscordUser (UserID, Discriminator, UserName, ShareData) "
                   "VALUES (?, ?, ?, ?)", user.id, user.discriminator, user.name, 0)
        db.commit()
        return


async def askData(ctx: ApplicationCommandInteraction, user: Member):
    await ctx.send("Desideri darci il consenso per salvare i tuoi dati?"
                             "\nRicorda che alcuni comandi hanno bisogno di questo consenso.\n"
                             "Rispondi con \"Si\" o \"No\"", ephemeral=True)
    message = await ctx.original_message()
    check = lambda m: m.author == user and m.channel == ctx.channel
    try:
        confirm = await GamingNetwork.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await message.edit(content="Ci hai impiegato troppo a inviarmi una risposta :pensive:")
        return
    if confirm.content.lower() == "si":
        await confirm.delete()
        await message.edit(content="Hai dato il consenso! procedo con il salvataggio")
        db.execute("UPDATE DiscordUser SET ShareData=? WHERE UserID IS ?", 1, ctx.author.id)
        db.commit()
        return
    elif confirm.content.lower() == "no":
        await confirm.delete()
        await message.edit(content="Ci dispiace di non essere degni della tua fiducia :pensive:")
    else:
        await confirm.delete()
        await message.edit(content="Non riesco ad analizzare la tua risposta :pensive:")
        return