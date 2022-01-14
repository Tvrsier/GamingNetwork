champList = [
    "Ahri",
    "Akali",
    "Akshan",
    "Alistar",
    "Amumu",
    "Annie",
    "Aurelion Sol",
    "Blitzcrank",
    "Brand",
    "Caitlyn",
    "Camille",
    "Corki",
    "Darius",
    "Diana",
    "Dr. Mundo",
    "Draven",
    "Evelynn",
    "Ezreal",
    "Fiora",
    "Fizz",
    "Galio",
    "Garen",
    "Gargas",
    "Graves",
    "Irelia",
    "Janna",
    "Jarvan IV",
    "Jax",
    "Jayce",
    "Jhin",
    "Jinx",
    'Khai\'Sa',
    "Katarina",
    "Kayle",
    "Kennen",
    'Kha\'Zix',
    "Lee Sin",
    "Leona",
    "Lucian",
    "Lulu",
    "Lux",
    "Malphite",
    "Master Yi",
    "Miss Fortune",
    "Morgana",
    "Nami",
    "Nasus",
    "Nunu & Willump",
    "Olaf",
    "Orianna",
    "Pantheon",
    "Rakan",
    "Rammus",
    "Renekton",
    "Rengar",
    "Riven",
    "Senna",
    "Seraphine",
    "Shyvana",
    "Singed",
    "Sona",
    "Soraka",
    "Teemo",
    "Thresh",
    "Tristana",
    "Tryndamere",
    "Twisted Fate",
    "Varus",
    "Vayne",
    "Veigar",
    "Vi",
    "Wukong",
    "Xayah",
    "Xin Zhao",
    "Yasuo",
    "Zed",
    "Ziggs",
]

roleList = [
    "Top", "Jungle", "Mid", "Bot", "Support"
]

rankList = [
    "Ferro", "Bronzo", "Argento", "Oro", "Platino", "Smeraldo", "Diamante", "Master", "Grand Master", "Challenger"
]


def checkChamps(champs: list|str) -> bool:
    if type(champs) == list:
        success = False
        for champ in champs:
            if champ in champList:
                success = True
        return True if success else False
    if type(champs) == str:
        return True if champs in champList else False


def checkRoles(roles: list|str) -> bool:
    if type(roles) == list:
        success = False
        for role in roles:
            if role in roleList:
                success = True
        return True if success else False
    else:
        return True if roles in roleList else False


def checkRank(rank: str) -> bool:
    return True if rank in rankList else False


