import requests

version = "2.51"
enablePrivateLogging = True
hide_names = True
hide_levels = True


gamemodes = {
    "newmap": "New Map",
    "competitive": "Competitive",
    "unrated": "Unrated",
    "swiftplay": "Swiftplay",
    "spikerush": "Spike Rush",
    "deathmatch": "Deathmatch",
    "ggteam": "Escalation",
    "onefa": "Replication",
    "custom": "Custom",
    "snowball": "Snowball Fight",
    "": "Custom",
}

before_ascendant_seasons = [
    "0df5adb9-4dcb-6899-1306-3e9860661dd3",
    "3f61c772-4560-cd3f-5d3f-a7ab5abda6b3",
    "0530b9c4-4980-f2ee-df5d-09864cd00542",
    "46ea6166-4573-1128-9cea-60a15640059b",
    "fcf2c8f4-4324-e50b-2e23-718e4a3ab046",
    "97b6e739-44cc-ffa7-49ad-398ba502ceb0",
    "ab57ef51-4e59-da91-cc8d-51a5a2b9b8ff",
    "52e9749a-429b-7060-99fe-4595426a0cf7",
    "71c81c67-4fae-ceb1-844c-aab2bb8710fa",
    "2a27e5d2-4d30-c9e2-b15a-93b8909a442c",
    "4cb622e1-4244-6da3-7276-8daaf1c01be2",
    "a16955a5-4ad0-f761-5e9e-389df1c892fb",
    "97b39124-46ce-8b55-8fd1-7cbf7ffe173f",
    "573f53ac-41a5-3a7d-d9ce-d6a6298e5704",
    "d929bc38-4ab6-7da4-94f0-ee84f8ac141e",
    "3e47230a-463c-a301-eb7d-67bb60357d4f",
    "808202d6-4f2b-a8ff-1feb-b3a0590ad79f",
]
sockets = {
    "skin": "bcef87d6-209b-46c6-8b19-fbe40bd95abc",
    "skin_level": "e7c63390-eda7-46e0-bb7a-a6abdacd2433",
    "skin_chroma": "3ad1b2b2-acdb-4524-852f-954a76ddae0a",
    "skin_buddy": "77258665-71d1-4623-bc72-44db9bd5b3b3",
    "skin_buddy_level": "dd3bf334-87f3-40bd-b043-682a57a8dc3a"
}


AGENTCOLORLIST = {
    "neon": 2,
    "none": 240,
    "viper": 42,
    "yoru": 20,
    "astra": 99,
    "breach": 209,
    "brimstone": 209,
    "cypher": 231,
    "jett": 68,
    "kay/o": 103,
    "killjoy": 179,
    "omen": 62,
    "phoenix": 205,
    "raze": 209,
    "reyna": 130,
    "sage": 12,
    "skye": 115,
    "sova": 28,
    "chamber": 232,
    "fade": 240
}


GAMEPODS = requests.get(
    "https://valorant-api.com/internal/locres/en-US").json()["data"]["UI_GamePodStrings"]


PARTYSYMBOL = "■"

PARTYICONLIST = [
    161,  # Red
    201,  # Pink
    27,  # Blue
    87,  # Teal
    83,  # Light Green
    227,  # Yellow
    200,
    251
]


NUMBERTORANKS = [
    ["Unranked", 238],
    ["Unranked", 238],
    ["Unranked", 238],

    ["Iron 1", 60],
    ["Iron 2", 60],
    ["Iron 3", 60],

    ["Bronze 1", 173],
    ["Bronze 2", 173],
    ["Bronze 3", 173],

    ["Silver 1", 252],
    ["Silver 2", 252],
    ["Silver 3", 252],

    ["Gold 1", 179],
    ["Gold 2", 179],
    ["Gold 3", 179],

    ["Platinum 1", 33],
    ["Platinum 2", 33],
    ["Platinum 3", 33],

    ["Diamond 1", 171],
    ["Diamond 2", 171],
    ["Diamond 3", 171],

    ["Ascendant 1", 29],
    ["Ascendant 2", 29],
    ["Ascendant 3", 29],

    ["Immortal 1", 13],
    ["Immortal 2", 13],
    ["Immortal 3", 13],

    ["Radiant", 230]
]

tierDict = {
    "0cebb8be-46d7-c12a-d306-e9907bfc5a25": 31,
    "e046854e-406c-37f4-6607-19a9ba8426fc": 216,
    "60bca009-4182-7998-dee7-b8a2558dc369": 127,
    "12683d76-48d7-84a3-4e09-6985794f0445": 33,
    "411e4a55-4e59-7757-41f0-86a53f101bb5": 227,
    None: None
}

WEAPONS = [
    "Classic",
    "Shorty",
    "Frenzy",
    "Ghost",
    "Sheriff",
    "Stinger",
    "Spectre",
    "Bucky",
    "Judge",
    "Bulldog",
    "Guardian",
    "Phantom",
    "Vandal",
    "Marshal",
    "Operator",
    "Ares",
    "Odin",
    "Melee",
]

DEFAULT_CONFIG = {
    "cooldown": 10,
    "port": 1100,
    "weapon": "Vandal",
    "table": {
        "skin": True,
        "rr": True,
        "peakrank": True,
        "leaderboard": True,
        "headshot_percent": True,
        "winrate": True,
        "kd": False
    },
    "flags": {
        "last_played": True,
        "auto_hide_leaderboard": True,
        "pre_cls": False,
        "game_chat": True,
        "peak_rank_act": True,
        "discord_rpc": True
    }
}
