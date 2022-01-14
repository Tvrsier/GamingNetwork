import pickle
from datetime import datetime
from os import path, rename
from typing import Optional, Any

from disnake import Embed, Colour, InteractionMessage, Message, User
from disnake.ext.commands import *

from lib.Games.WildRift.User import WRUser
from lib.bot.UserChecks.Checks import checkData, checkWR_Found, checkWR_NotFound
from lib.bot.askData import *
from ..db import db

picklePath = "./data/pickle/WR"


class WildRift(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="wr", description="Comandi wild rift", guild_ids=[865691556736008213])
    @checkData()
    async def wr(self, ctx: ApplicationCommandInteraction):
        pass

    @wr.sub_command(name="user_info", description="Leggi le tue informazioni o quelle di un altro utente",
                    guild_ids=[865691556736008213])
    @checkWR_Found()
    async def user_info(self, ctx: ApplicationCommandInteraction, user: Optional[Member] = None):
        if user is not None:
            # if path.exists(f"{picklePath}/{user.name}{user.discriminator}.obj"):
            #     user_path = f"{picklePath}/{user.name}{user.discriminator}.obj"
            # else:
            #     await ctx.send("Questo utente non è registrato a Wild Rift")
            #     return

            user_path = self.conc_path(user.name, user.discriminator) if \
                path.exists(self.conc_path(user.name, user.discriminator)) else \
                await ctx.send("Questo utente non è registrato a WIld Rift")
        else:
            user_path = f"{picklePath}/{ctx.author.name}{ctx.author.discriminator}.obj"
        WR_User: WRUser = await self.load_obj(user_path)
        embed = Embed(title=f"GamingNetwork | {WR_User.UserName} User Info",
                      colour=Colour.random(),
                      timestamp=datetime.utcnow(),
                      description="\u00AD")
        embed.set_footer(text="Gaming Network | By Tvrsier", icon_url=self.bot.user.avatar.url)
        for name, value, inline in WR_User.info():
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)

    @wr.sub_command(name="update", description="Aggiorna i tuoi dati (sovrascrive quelli già esistenti)",
                    guild_ids=[865691556736008213])
    @checkWR_Found()
    async def update(self, ctx: ApplicationCommandInteraction, champs: str = None, roles: str = None, rank: str = None):
        embed = Embed(title=f"GamingNetwork | Update",
                      colour=Colour.random(),
                      description="\u00AD",
                      timestamp=datetime.utcnow())
        embed.set_footer(text="Gaming Network | By Tvrsier", icon_url=self.bot.user.avatar.url)
        if champs is None and roles is None and rank is None:
            await ctx.send("Devi riempire almeno uno di questi campi per usare questo comando", ephemeral=True)
        else:
            WR_User: WRUser = await self.load_obj(self.conc_path(ctx.author.name, ctx.author.discriminator))
            if champs is not None:
                if ", " in champs:
                    champs = champs.title().split(", ")
                else:
                    champs = champs.title()
            if roles is not None:
                if ", " in roles:
                    roles = roles.title().split(", ")
                else:
                    roles = roles.title()
            if rank is not None:
                rank = rank.title()
            WR_User.update(champs=champs, roles=roles, rank=rank)
            for name, value, inline in WR_User.info():
                embed.add_field(name=name, value=value, inline=inline)
            await self.save_obj(WR_User, self.conc_path(ctx.author.name, ctx.author.discriminator))
            await ctx.send(embed=embed, ephemeral=True)

    @wr.sub_command(name="add", description="Aggiungi Campioni o Ruoli ai tuoi attuali", guild_ids=[865691556736008213])
    @checkWR_Found()
    async def add(self, ctx: ApplicationCommandInteraction, champs: str = None, roles: str = None):
        embed = Embed(title=f"GamingNetwork | Add",
                      colour=Colour.random(),
                      description="\u00AD",
                      timestamp=datetime.utcnow())
        embed.set_footer(text="Gaming Network | By Tvrsier", icon_url=self.bot.user.avatar.url)
        if champs is not None or roles is not None:
            WR_User: WRUser = await self.load_obj(self.conc_path(ctx.author.name, ctx.author.discriminator))
            if champs is not None:
                if ", " in champs:
                    champs = champs.title().split(", ")
                else:
                    champs = champs.title()
            if roles is not None:
                if ", " in roles:
                    roles = roles.title().split(", ")
                else:
                    roles = roles.title()
            WR_User.add(champs=champs, roles=roles)
            for name, value, inline in WR_User.info():
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed, ephemeral=True)
            await self.save_obj(WR_User, self.conc_path(ctx.author.name, ctx.author.discriminator))
        else:
            await ctx.send("Devi inserire almeno uno dei due parametri per usare questo comando")

    @wr.sub_command(name="register", description="Inserisci i tuoi dati di Wild Rift", guild_ids=[865691556736008213])
    @checkWR_NotFound()
    async def register(self, ctx: ApplicationCommandInteraction):
        embed = Embed(title=f"Benvenuto in GamingNetwork {ctx.author.name}",
                      timestamp=datetime.now(),
                      colour=Colour.random(),
                      description="\u00AD")
        embed.add_field(name=f"Registrazione user {ctx.author.id}",
                        value="Iniziamo la fase di registrazione per il tuo utente Wild Rift!\n"
                              "Quando sei pronto digita \"Sono pronto\"",
                        inline=False,
                        )
        embed.set_footer(text="Gaming Network | By Tvrsier", icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed, ephemeral=True)
        check_msg = lambda m: m.author == ctx.author and m.channel == ctx.channel
        original_interaction: InteractionMessage = await ctx.original_message()
        try:
            confirm: Message = await self.bot.wait_for('message', check=check_msg, timeout=60)
        except asyncio.TimeoutError:
            embed.set_field_at(index=0,
                               name=f"Registrazione user {ctx.author.id}",
                               value="Hey! Mica posso aspettarti in eterno. Ci hai impiegato troppo, riprova",
                               inline=False)
            await original_interaction.edit(embed=embed)
            return
        if confirm.content.lower() == "sono pronto":
            await confirm.delete()
            embed.set_field_at(index=0,
                               name=f"Registrazione user {ctx.author.id}",
                               value="Dunque cominciamo!\n"
                                     "Scrivi il tuo Username e il tuo ID di Wild Rift (Username#ID)",
                               inline=False)
            await original_interaction.edit(embed=embed)
            try:
                confirm: Message = await self.bot.wait_for("message", check=check_msg, timeout=90)
            except asyncio.TimeoutError:
                embed.set_field_at(index=0,
                                   name=f"Registrazione user {ctx.author.id}",
                                   value="Hey! Mica posso aspettarti in eterno. Ci hai impiegato troppo. Riprova",
                                   inline=False)
                await original_interaction.edit(embed=embed)
                return
            if confirm.content[-4:].isdigit() and confirm.content[-5] == "#":
                await confirm.delete()
                WR_UserName, WR_ID = confirm.content.split("#")
                WR_User = WRUser(WR_ID, WR_UserName, ctx.author.id)
                db.execute("INSERT INTO WildRiftUser(DiscordID, UserID, UserName) "
                           "VALUES(?, ?, ?)", ctx.author.id, WR_User.UserID, WR_User.UserName)
                db.commit()
            elif len(confirm.content.split()) > 1:
                await confirm.delete()
                embed.set_field_at(index=0,
                                   name=f"Registrazione user {ctx.author.id}",
                                   value="Ti ho chiesto il tuo utente di Wild Rift, non di scrivermi una poesia",
                                   inline=False)
                await original_interaction.edit(embed=embed)
                return
            else:
                await confirm.delete()
                embed.set_field_at(index=0,
                                   name=f"Registrazione user {ctx.author.id}",
                                   value="Credi che io sia scemo? So benissimo che quello non è un utente di Wild Rift",
                                   inline=False)
                await original_interaction.edit(embed=embed)
                return
            result = [False, False, False]
            embed.set_field_at(index=0,
                               name=f"Registrazione user {ctx.author.id}",
                               value="Perfetto. Abbiamo completato la prima parte della tua registrazione. "
                                     "I dati che ti chiederò da ora sono opzionali, ma ricorda che possono servire "
                                     "per aiutarti a trovare altri giocatori che siano più affini a te. Potrai"
                                     "comunque modificare o aggiungere questi dati più tardi."
                                     "Vuoi inserire i campioni che usi?",
                               inline=False
                               )
            await original_interaction.edit(embed=embed)
            try:
                confirm: Message = await self.bot.wait_for("message", check=check_msg, timeout=30)
            except asyncio.TimeoutError:
                embed.set_field_at(index=0,
                                   name=f"Registrazione user {ctx.author.id}",
                                   value="Hey! Mica posso aspettarti in eterno. Ci hai impiegato troppo. Riprova",
                                   inline=False)
                await original_interaction.edit(embed=embed)
                return
            if confirm.content.lower() == "si" or confirm.content.lower() == "certo":
                await confirm.delete()
                embed.set_field_at(index=0,
                                   name=f"Registrazione user {ctx.author.id}",
                                   value="Bene allora. Adesso scrivi quali sono i campioni che usi (Ricorda "
                                         "di mantenere gli spazi (ES: Aurelion Sol) e gli apostrofi (ES: Kha'Zix)"
                                         " separando ogni campione con una virgola (ES: Aurelion Sol, Kha'Zix, Akali)",
                                   inline=False)
                await original_interaction.edit(embed=embed)
                try:
                    confirm: Message = await self.bot.wait_for("message", check=check_msg, timeout=180)
                except asyncio.TimeoutError:
                    embed.set_field_at(index=0,
                                       name=f"Registrazione user {ctx.author.id}",
                                       value="Hey! Mica posso aspettarti in eterno. Ci hai impiegato troppo. Riprova",
                                       inline=False)
                    await original_interaction.edit(embed=embed)
                    return
                if ", " in confirm.content:
                    await confirm.delete()
                    champ_list = confirm.content.title().split(", ")
                    result[0] = WR_User.update(champs=champ_list)[0]
                    # print(f"User champs from command: {WR_User.Champs}")
                else:
                    await confirm.delete()
                    result[0] = WR_User.update(champs=confirm.content)[0]
                if result[0]:
                    embed.add_field(name="Campioni", value=f"{', '.join(WR_User.Champs)}. "
                                                           "(Quelli che sono risultati errati non sono stati aggiunti, "
                                                           "quando avrai finito potrai controllare con /wr user_info)",
                                    inline=True)
                else:
                    embed.add_field(name="Campioni", value="Sembra che tu abbia inserito dei campioni errati, potrai "
                                                           "provare ad inserirli più tardi.", inline=True)
            elif confirm.content.lower() == "no":
                await confirm.delete()
                embed.add_field(name="Campioni", value="N/A", inline=True)
            else:
                await confirm.delete()
                embed.add_field(name="Campioni", value="Non ho capito bene cosa hai scritto :pensive:", inline=True)
            embed.set_field_at(index=0,
                               name=f"Registrazione user {ctx.author.id}",
                               value="Bene, ora dimmi se vuoi inserire i ruoli in cui giochi",
                               inline=False)
            await original_interaction.edit(embed=embed)
            try:
                confirm: Message = await self.bot.wait_for("message", check=check_msg, timeout=30)
            except asyncio.TimeoutError:
                embed.set_field_at(index=0,
                                   name=f"Registrazione user {ctx.author.id}",
                                   value="Hey! Mica posso aspettarti in eterno. Ci hai impiegato troppo. Riprova",
                                   inline=False)
                await original_interaction.edit(embed=embed)
                return
            if confirm.content.lower() == "si" or confirm.content.lower() == "certo":
                await confirm.delete()
                embed.set_field_at(index=0,
                                   name=f"Registrazione user {ctx.author.id}",
                                   value="Allora scrivi i ruoli in cui giochi, la modalità è la stessa per i campioni, "
                                         "separa con una virgola ogni ruolo",
                                   inline=False)
                await original_interaction.edit(embed=embed)
                try:
                    confirm: Message = await self.bot.wait_for("message", check=check_msg, timeout=180)
                except asyncio.TimeoutError:
                    embed.set_field_at(index=0,
                                       name=f"Registrazione user {ctx.author.id}",
                                       value="Hey! Mica posso aspettarti in eterno. Ci hai impiegato troppo. Riprova",
                                       inline=False)
                    await original_interaction.edit(embed=embed)
                    return
                if ", " in confirm.content:
                    await confirm.delete()
                    role_list = confirm.content.title().split(", ")
                    result[1] = WR_User.update(roles=role_list)
                    # print(f"WR Roles from command: {WR_User.Roles}")
                else:
                    await confirm.delete()
                    result[1] = WR_User.update(roles=confirm.content)
                if result[1]:
                    embed.add_field(name="Ruoli",
                                    value=f"{', '.join(WR_User.Roles)}\n (Quelli scritti in modo errato non "
                                          "sono aggiunti, quando hai finito controlla con "
                                          "/wr user_info", inline=True)
            elif confirm.content.lower() == "no":
                await confirm.delete()
                embed.add_field(name="Ruoli", value="N/A", inline=True)
            else:
                await confirm.delete()
                embed.add_field(name="Ruoli", value="Non ho capito bene cosa hai scritto :pensive:", inline=True)
            embed.set_field_at(index=0,
                               name=f"Registrazione user {ctx.author.id}",
                               value="E ora l'ultimo passaggio! Questo è obbligatorio. Inserisci il tuo ELO (Rank) "
                                     "attuale in Wild Rift",
                               inline=False)
            await original_interaction.edit(embed=embed)
            try:
                confirm: Message = await self.bot.wait_for("message", check=check_msg, timeout=120)
            except asyncio.TimeoutError:
                embed.set_field_at(index=0,
                                   name=f"Registrazione user {ctx.author.id}",
                                   value="Hey! Mica posso aspettarti in eterno. Ci hai impiegato troppo. Riprova",
                                   inline=False)
            await confirm.delete()
            result[2] = WR_User.update(rank=confirm.content.title())
            # print(f"User Rank from command: {WR_User.Rank}")
            if result[2]:
                embed.add_field(name="Rank", value=f"{WR_User.Rank}", inline=True)
            else:
                embed.add_field(name="Rank", value="Il rank che hai inserito non esiste in Wild Rift", inline=True)
            embed.set_field_at(index=0,
                               name=f"Registrazione user {ctx.author.id}",
                               value="Abbiamo terminato! Ora il tuo account è stato registrato\n"
                                     "Ricorda che puoi controllare i tuoi dati con /wr user_info "
                                     "e quelli degli altri con /wr user_info [user]",
                               inline=False)
            filename = f"{picklePath}/{ctx.author.name}{ctx.author.discriminator}.obj"
            await self.save_obj(WR_User, filename)
            WR_User_pickle: WRUser = await self.load_obj(filename)
            # print(f"User object from pickle: {WR_User_pickle.info()}")
            await original_interaction.edit(embed=embed)
        elif confirm.content.lower() == "non sono pronto":
            await confirm.delete()
            embed.set_field_at(index=0,
                               name=f"Registrazione user {ctx.author.id}",
                               value="Digita di nuovo questo comando quando vorrai registrarti",
                               inline=False)
            await original_interaction.edit(embed=embed)

    @Cog.listener()
    async def on_user_update(self, before: User, after: User):
        if before.name != after.name or before.discriminator != after.discriminator:
            if path.exists(self.conc_path(before.name, before.discriminator)):
                old_path = self.conc_path(before.name, before.discriminator)
                new_path = self.conc_path(after.name, after.discriminator)
                rename(old_path, new_path)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("WildRift")

    @staticmethod
    async def save_obj(obj: object, filename: str):
        with open(filename, 'wb') as save_file:
            pickle.dump(obj, save_file)

    @staticmethod
    async def load_obj(filename: str) -> Any:
        with open(filename, 'rb') as load_file:
            return pickle.load(load_file)

    @staticmethod
    def conc_path(username, userdiscriminator) -> str:
        return f"{picklePath}/{username}{userdiscriminator}.obj"


def setup(bot):
    bot.add_cog(WildRift(bot))
