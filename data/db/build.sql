CREATE TABLE IF NOT EXISTS guilds (
    GuildID integer PRIMARY KEY,
    Prefix text DEFAULT "!"
);

CREATE TABLE IF NOT EXISTS games (
    GameID integer PRIMARY KEY,
    GameName text NOT NULL 
);