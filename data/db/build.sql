CREATE TABLE IF NOT EXISTS Guild(
    GuildID integer PRIMARY KEY,
    Name text DEFAULT NULL,
    LogChannelID integer DEFAULT NULL,
    FeedbackChannelID integer DEFAULT NULL,
    WelcomeMessage integer DEFAULT 0
);

CREATE TABLE IF NOT EXISTS DiscordUser (
    UserID integer PRIMARY KEY,
    Discriminator INTEGER,
    UserName text DEFAULT NULL,
    ShareData INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS WildRiftUser (
    DiscordID INTEGER PRIMARY KEY,
    UserID INTEGER NOT NULL,
    UserName TEXT NOT NULL,
    Champs TEXT DEFAULT NULL,
    Roles TEXT DEFAULT NULL,
    Rank TEXT DEFAULT NULL
);