from CheckData import checkRank, checkRoles, checkChamps
from ...db import db

class User():
    def __init__(self, UserID: int, UserName: str, Champs: list = None, Rank: str=None, Roles: list=None):
        self.UserID = UserID
        self.UserName = UserName
        self.Champs = Champs if Champs is not None else []
        self.Rank = Rank
        self.Roles = Roles if Roles is not None else []
        self.picke_path = "..../data/pickle/WR/"

    @staticmethod
    def is_champ(champ: list|str):
        return checkChamps(champ)

    @staticmethod
    def is_rank(rank: str):
        return checkRank(rank)

    @staticmethod
    def is_role(role: list|str):
        return checkRoles(role)

    def update(self, champs: list|str = None, roles: list|str = None, rank: str = None) -> list:
        success = [(False, False, False)]
        if champs is not None and self.is_champ(champs):
            success[[0][0]] = True
            if type(champs) == list:
                self.Champs = champs
            else:
                self.Champs = []
                self.Champs[0] = champs
            db.execute("UPDATE WildRiftUser SET Champs=? (?) WHERE DiscordID IS ?",
                       ", ".join(self.Champs), self.UserID)
            db.commit()
        if roles is not None and self.is_role(roles):
            success[[0][1]] = True
            if type(roles) == list:
                self.Roles = roles
            else:
                self.Roles = []
                self.Roles[0] = roles
            db.execute("UPDATE WildRiftUser SET Roles=? WHERE DiscordID IS ?",
                       ", ".join(self.Roles), self.UserID)
            db.commit()
        if rank is not None and self.is_rank(rank):
            success[[0][2]] = True
            self.Rank = rank
            db.execute("UPDATE WildRiftUser SET Rank=? WHERE DiscordID IS ?", self.Rank, self.UserID)
            db.commit()
        return success

    def add(self, champs: list|str = None, roles: list|str = None) -> list:
        success = [(False, False)]
        if champs is not None and self.is_champ(champs):
            if type(champs) == list:
                for champ in champs:
                    if champ not in self.Champs:
                        self.Champs.append(champ)
                        success[[0][0]] = True
            else:
                if champs not in self.Champs:
                    self.Champs.append(champs)
            if success[[0][0]]:
                db.execute("UPDATE WildRiftUser SET Champs=? WHERE DiscordID IS ?",
                           ", ".join(self.Champs), self.UserID)
                db.commit()
        if roles is not None and self.is_role(roles):
            if type(roles) == list:
                for role in roles:
                    if role not in self.Roles:
                        self.Roles.append(role)
                        success[[0][1]] = True
            else:
                if roles not in self.Roles:
                    self.Roles.append(roles)
                    success[[0][1]] = True
            if success[[0][1]]:
                db.execute("UPDATE WildRiftUser SET Roles=? WHERE DiscordID IS ?",
                           ", ".join(self.Roles), self.UserID)
                db.commit()
        return success

    def delete(self, champs: list|str = None, roles: list|str = None, rank: str = None) -> list:
        success = [(False, False, False)]
        if champs is not None and self.is_champ(champs):
            if type(champs) == list:
                for champ in champs:
                    if champ in self.Champs:
                        self.Champs.remove(champ)
                        success[[0][0]] = True
            else:
                if champs in self.Champs:
                    self.Champs.remove(champs)
                    success[[0][0]] = True
            if success[[0][0]]:
                if self.Champs:
                    db.execute("UPDATE WildRiftUser SET Champs=? WHERE DiscordID IS ?",
                               ", ".join(self.Champs), self.UserID)
                else:
                    db.execute("UPDATE WildRiftUser SET Champs=NULL Where DiscordID IS ?", self.UserID)
                db.commit()
        if roles is not None and self.is_role(roles):
            if type(roles) == list:
                for role in roles:
                    if role in self.Roles:
                        self.Roles.remove(role)
                        success[[0][1]] = True
            else:
                if roles in self.Roles:
                    self.Roles.remove(roles)
                    success[[0][1]] = True
            if success[[0][1]]:
                if self.Roles:
                    db.execute("UPDATE WildRiftUser SET Roles=? WHERE DiscordID IS ?",
                               ", ".join(self.Roles), self.UserID)
                else:
                    db.execute("UPDATE WildRiftUser SET Roles=NULL WHERE DiscordID IS ?", self.UserID)
                db.commit()
        if rank is not None and self.is_rank(rank):
            if rank not in self.Rank:
                self.Rank = None
                success[[0][3]] = True
            if success[[0][3]]:
                db.execute("UPDATE WildRiftUser SET Rank=NULL WHERE DiscordID IS ?", self.UserID)
                db.commit()
        return success

    def info(self):
        tuple_list = [(self.UserID), (self.UserName), (self.Champs), (self.Roles), (self.Champs)]
        return tuple_list
