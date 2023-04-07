import curses
import asyncio
import time
import os
import requests
import math
import urllib3
import psutil
import threading
import traceback
from src.TermUI.src.TermUI.button import Button
from src.TermUI.src.TermUI.ui import UI
from src.TermUI.src.TermUI.region import Region
from src.TermUI.src.TermUI.position import Position
from src.TermUI.src.TermUI.text import Text
from src.TermUI.src.TermUI.region import BoxCharacters
from src.TermUI.src.TermUI.button import Button
from src.constants import *
from src.requestsV import Requests
from src.logs import Logging
from src.config import Config
from src.colors import Colors
from src.rank import Rank
from src.content import Content
from src.names import Names
from src.presences import Presences
from src.Loadouts import Loadouts
from src.websocket import Ws


from src.states.menu import Menu
from src.states.pregame import Pregame
from src.states.coregame import Coregame

from src.table import Table
from src.server import Server
from src.errors import Error

from src.stats import Stats
from src.configurator import configure
from src.player_stats import PlayerStats

from src.chatlogs import ChatLogging

from src.rpc import Rpc

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    os.system(f"title vRY v{version}")
    INACTIVE_RED = 161
    WARNING_YELLOW = 179
    SUCCESS_GREEN = 84

    HIGHLIGHTED_TAB = 204

    threads = list()

    loading_ui = UI(stdscr)
    loading_region = Region("", Position(0, 0), Position(119, 29))
    loading_region.framed = False
    loading_ui.add_region(loading_region)

    ascii_art = ["    ▄   █▄▄▄▄ ▀▄    ▄ ",
                 "     █  █  ▄▀   █  █  ", "█     █ █▀▀▌     ▀█   ", " █    █ █  █     █    ", "  █  █    █    ▄▀     ", "   █▐    ▀            ", "   ▐                  "]

    for i, line in enumerate(ascii_art):
        position = Position(loading_region.size.half().x-len(line)+12,
                            loading_region.size.half().y-len(ascii_art)+i)
        text_element = Text(line, position)
        text_element.color = HIGHLIGHTED_TAB
        loading_region.add_element(text_element)

    subtitle_string = f"Valorant rank yoinker v{version} is initializing"
    subtitle = Text(subtitle_string, Position(
        loading_region.size.half().x - len(subtitle_string) + 19,
        loading_region.size.half().y))
    subtitle.color = WARNING_YELLOW
    loading_region.add_element(subtitle)

    loading_status = Text("Loading vRY...", Position(
        loading_region.size.half().x - len(subtitle_string) + 19,
        loading_region.size.half().y+1))
    loading_status.color = SUCCESS_GREEN

    loading_region.add_element(loading_status)

    loading_ui.draw()

    main_ui = UI(stdscr)

    loaded_players = []

    tab_region = Region("", Position(0, 0), Position(119, 29))
    tab_region.framed = False
    main_ui.add_region(tab_region)

    def disable_all_tabs():
        for region in content_regions:
            content_regions[region].visible = False

    def highlight_button(button):
        for tab in tabs:
            tab.color = tab.region.ui.default_color
        button.color = HIGHLIGHTED_TAB

    def ally_tab(button):
        disable_all_tabs()
        content_regions.get("ally_scoreboard").visible = True
        for region in scoreboard_regions.get("ally"):
            region.visible = True
        for region in scoreboard_regions.get("enemy"):
            region.visible = False
        highlight_button(button)
        main_ui.draw()

    def enemy_tab(button):
        disable_all_tabs()
        content_regions.get("enemy_scoreboard").visible = True
        for region in scoreboard_regions.get("enemy"):
            region.visible = True
        for region in scoreboard_regions.get("ally"):
            region.visible = False
        highlight_button(button)
        main_ui.draw()

    def skins_tab(button):
        disable_all_tabs()
        content_regions.get("skins").visible = True
        highlight_button(button)
        main_ui.draw()

    def chat_tab(button):
        disable_all_tabs()
        content_regions.get("chat").visible = True
        highlight_button(button)
        main_ui.draw()

    scoreboard_regions = dict(ally=list(), enemy=list())
    content_regions = {
        "ally_scoreboard": Region(
            "", Position(0, 2), Position(119, 29)),
        "enemy_scoreboard": Region(
            "", Position(0, 2), Position(119, 29)),
        "skins": Region(
            "", Position(0, 2), Position(119, 29)),
        "chat": Region(
            "", Position(0, 2), Position(119, 29))
    }
    offset = content_regions.get("ally_scoreboard").start + Position(1, 3)

    def update_loading_player_count(loaded: list):
        player_loading_status.set_text(
            f"Loading players [{loaded[0]}/{loaded[1]}]")
        player_loading_status.color = WARNING_YELLOW
        player_loading_status.hidden = False
        player_loading_status.start = content_regions.get(
            "ally_scoreboard").sOrigin + Position(1, 0)
        if loaded[0] > loaded[1]:
            player_loading_status.hidden = True
        main_ui.draw()

    def even_centered(xPos: int):
        if xPos % 2 == 0:
            return xPos + 1
        return xPos

    def draw_player(data: dict, loaded: list):
        nonlocal offset
        xSpace = math.ceil(
            (content_regions.get("ally_scoreboard").size.x-2)/5)

        update_loading_player_count(loaded)
        # ally screen
        if loaded[0] <= 5:
            if game_state == "MENUS":
                if data['puuid'] in loaded_players:
                    return
                player_region = Region(data['name'], offset, Position(
                    xSpace, content_regions.get("ally_scoreboard").size.y-3))
                entries = {
                    'name': {
                        'text': data['name'].split("#")[0],
                        'position': Position(
                            player_region.size.half().x -
                            math.floor(
                                len(data['name'].split("#")[0])/2)-1,
                            2
                        ),
                        'color': 0
                    },
                    'rank': {
                        'text': f"{data['rankName'][0]} {data['rr']}rr",
                        'position': Position(
                            player_region.size.half().x -
                            math.floor(
                                len(f"{data['rankName'][0]} {data['rr']}rr")/2)-1,
                            5
                        ),
                        'color': data['rankName'][1]
                    },
                    'peak': {
                        'text': f"\u0394 {data['peak'][0][0]}{data['peak'][1]}",
                        'position': Position(
                            player_region.size.half().x -
                            math.floor(
                                len(f"\u0394 {data['peak'][0][0]}{data['peak'][1]}")/2)-1,
                            6
                        ),
                        'color': data['peak'][0][1]
                    },
                    'hs': {
                        'text': f"HS: {data['hs'][0]}%",
                        'position': Position(
                            player_region.size.half().x -
                            math.floor(
                                len(f"HS: {data['hs'][0]}%")/2)-1,
                            8
                        ),
                        'color': data['hs'][1]
                    },
                    'wr': {
                        'text': f"WR: {data['wr'][0][0]}%{data['wr'][1]}",
                        'position': Position(
                            player_region.size.half().x -
                            math.floor(
                                len(f"WR: {data['wr'][0][0]}%{data['wr'][1]}")/2)-1,
                            9
                        ),
                        'color': data['wr'][0][1]
                    },
                    'kd': {
                        'text': f"KD: {data['kd'][0]}",
                        'position': Position(
                            player_region.size.half().x -
                            math.floor(
                                len(f"KD: {data['kd'][0]}")/2)-1,
                            10
                        ),
                        'color': data['kd'][1]
                    }
                }
                for item in entries:
                    print(item)
                    item = entries[item]
                    element = Text(
                        item['text'], item['position'])
                    if item['color'] > 0:
                        element.color = item['color']

                    player_region.add_element(element)
                print(player_region.elements)

                main_ui.add_region(player_region)
                scoreboard_regions.get("ally").append(player_region)
                offset += Position(xSpace, 0)

                if loaded[0] == 5:
                    offset = content_regions.get(
                        "enemy_scoreboard").start + Position(1, 3)

        if loaded[0] > 5:
            ...
        main_ui.draw()

    tab_offset = Position(-1, -1)
    pretabs = {
        "Allies": ally_tab,
        "Enemies": enemy_tab,
        "Skins": skins_tab,
        "Chat": chat_tab
    }

    player_loading_status = Text('', Position(0, 0))
    player_loading_status.hidden = True

    tab_region.add_element(player_loading_status)

    loading_status.set_text("Creating UI...")
    loading_ui.draw()

    tabs = []
    for name in pretabs:
        created = Button(name, tab_offset, pretabs[name])
        tabs.append(created)
        tab_region.add_element(created)
        tab_offset += Position(created.size.x + 1, 0)

    tabs[0].color = HIGHLIGHTED_TAB

    for region in content_regions:
        main_ui.add_region(content_regions.get(region))

    disable_all_tabs()

    content_regions['ally_scoreboard'].visible = True

    # content_regions.get("scoreboard").add_element(
    #    Text("Scoreboard", Position(0, 0)))
    content_regions.get("skins").add_element(
        Text("Skins", Position(0, 0)))
    content_regions.get("chat").add_element(
        Text("Chat", Position(0, 0)))

    waiting = True

    def redraw_load():
        while waiting:
            loading_status.set_text("Waiting for valorant...")
            loading_ui.draw()
            time.sleep(3)
        curses.curs_set(0)
        curses.mousemask(1)

    waiting_thread = threading.Thread(
        target=redraw_load, args=(), daemon=True)

    waiting_thread.start()

    logger = Logging
    log = logger.log
    chatLogging = ChatLogging()
    chatlog = chatLogging.chatLog
    ErrorSRC = Error(log)
    req = Requests(version, log, ErrorSRC)
    req.check_version()
    req.check_status()
    cfg = Config(log)
    content = Content(req, log)
    rank = Rank(req, log, content, before_ascendant_seasons)
    pstats = PlayerStats(req, log, cfg)
    namesClass = Names(req, log)
    presences = Presences(req, log)
    menu = Menu(req, log, presences)
    pregame = Pregame(req, log)
    coregame = Coregame(req, log)
    server = Server(log, ErrorSRC)
    server.start_server()
    agent_dict = content.get_all_agents()
    map_dict = content.get_maps()
    colors = Colors(hide_names, agent_dict, AGENTCOLORLIST)
    loadoutsClass = Loadouts(req, log, colors, Server)
    table = Table(cfg, chatlog, log)
    stats = Stats()
    if cfg.get_feature_flag("discord_rpc"):
        rpc = Rpc(map_dict, gamemodes, colors, log)
    else:
        rpc = None
    Wss = Ws(req.lockfile, req, cfg,
             colors, hide_names, chatlog, rpc)
    log(f"VALORANT rank yoinker v{version}")
    valoApiSkins = requests.get("https://valorant-api.com/v1/weapons/skins")
    gameContent = content.get_content()
    seasonID = content.get_latest_season_id(gameContent)
    lastGameState = ""
    presence = None
    waiting = False

    # print(color("\nVisit https://vry.netlify.app/matchLoadouts to view full player inventories\n", fore=(255, 253, 205)))
    # chatlog(color("\nVisit https://vry.netlify.app/matchLoadouts to view full player inventories\n", fore=(255, 253, 205)))

    loading_status.set_text("Creating discord RPC")
    loading_ui.draw()
    run = True
    while run:
        while True:
            presence = presences.get_presence()
            # wait until your own valorant presence is initialized
            if presences.get_private_presence(presence) != None:
                break
            time.sleep(5)
        if cfg.get_feature_flag("discord_rpc"):
            rpc.set_rpc(presences.get_private_presence(presence))
        game_state = presences.get_game_state(presence)
        if game_state != None:
            run = False
        time.sleep(2)
    log(f"first game state: {game_state}")

    rpc_status = Text("", Position(0, 0))

    tab_region.add_element(rpc_status)
    kill_threads = False

    def update_rpc():
        nonlocal game_state

        while True:
            try:
                rpc_status.set_text("● RPC Running")
                rpc_status.color = SUCCESS_GREEN
                rpc_status.start = Position(content_regions.get(
                    "ally_scoreboard").size.x-2-len(rpc_status.text), 3)
                rpc_status.draw()
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                game_state = loop.run_until_complete(
                    Wss.recconect_to_websocket(game_state))
                log(f"new game state: {game_state}")
                loop.close()
                if kill_threads:
                    break
            except Exception as e:
                main_ui.deactivate()
                print(e)
                rpc_status.color = INACTIVE_RED
                rpc_status.set_text("● RPC Lost")

    def game_state_loop():
        nonlocal presence
        nonlocal rpc
        nonlocal loaded_players
        nonlocal game_state
        nonlocal rpc_status
        try:
            log(f"getting new {game_state} scoreboard")
            lastGameState = game_state
            game_state_dict = {
                "INGAME": 'In-Game',
                "PREGAME": 'Agent Select',
                "MENUS": 'In-Menus',
            }

            is_leaderboard_needed = False
            while True:
                if game_state == "INGAME":
                    coregame_stats = coregame.get_coregame_stats()
                    if coregame_stats == None:
                        continue
                    Players = coregame_stats["Players"]
                    # data for chat to function
                    presence = presences.get_presence()
                    partyMembers = menu.get_party_members(req.puuid, presence)
                    partyMembersList = [a["Subject"] for a in partyMembers]

                    players_data = {}
                    players_data.update({"ignore": partyMembersList})
                    for player in Players:
                        if player["Subject"] == req.puuid:
                            if cfg.get_feature_flag("discord_rpc"):
                                rpc.set_data({"agent": player["CharacterID"]})
                        players_data.update({player["Subject"]: {
                                            "team": player["TeamID"], "agent": player["CharacterID"], "streamer_mode": player["PlayerIdentity"]["Incognito"]}})
                    Wss.set_player_data(players_data)

                    try:
                        server = GAMEPODS[coregame_stats["GamePodID"]]
                    except KeyError:
                        server = "New server"
                    presences.wait_for_presence(
                        namesClass.get_players_puuid(Players))
                    names = namesClass.get_names_from_puuids(Players)
                    loadouts = loadoutsClass.get_match_loadouts(coregame.get_coregame_match_id(
                    ), Players, cfg.weapon, valoApiSkins, names, state="game")
                    # with alive_bar(total=len(Players), title='Fetching Players', bar='classic2') as bar:
                    isRange = False
                    playersLoaded = 1
                    partyOBJ = menu.get_party_json(
                        namesClass.get_players_puuid(Players), presence)
                    # log(f"retrieved names dict: {names}")
                    Players.sort(key=lambda Players: Players["PlayerIdentity"].get(
                        "AccountLevel"), reverse=True)
                    Players.sort(
                        key=lambda Players: Players["TeamID"], reverse=True)
                    partyCount = 0
                    partyIcons = {}
                    lastTeamBoolean = False
                    lastTeam = "Red"

                    already_played_with = []
                    stats_data = stats.read_data()

                    for p in Players:
                        if p["Subject"] == req.puuid:
                            allyTeam = p["TeamID"]
                    for player in Players:
                        playersLoaded += 1

                        if player["Subject"] in stats_data.keys():
                            if player["Subject"] != req.puuid and player["Subject"] not in partyMembersList:
                                curr_player_stat = stats_data[player["Subject"]][-1]
                                i = 1
                                while curr_player_stat["match_id"] == coregame.match_id and len(stats_data[player["Subject"]]) > i:
                                    i += 1
                                # if curr_player_stat["match_id"] == coregame.match_id and len(stats_data[player["Subject"]]) > 1:
                                    curr_player_stat = stats_data[player["Subject"]][-i]
                                if curr_player_stat["match_id"] != coregame.match_id:
                                    # checking for party memebers and self players
                                    times = 0
                                    m_set = ()
                                    for m in stats_data[player["Subject"]]:
                                        if m["match_id"] != coregame.match_id and m["match_id"] not in m_set:
                                            times += 1
                                            m_set += (m["match_id"],)
                                    if player["PlayerIdentity"]["Incognito"] == False:
                                        already_played_with.append(
                                            {
                                                "times": times,
                                                "name": curr_player_stat["name"],
                                                "agent": curr_player_stat["agent"],
                                                "time_diff": time.time() - curr_player_stat["epoch"]
                                            })
                                    else:
                                        if player["TeamID"] == allyTeam:
                                            team_string = "your"
                                        else:
                                            team_string = "enemy"
                                        already_played_with.append(
                                            {
                                                "times": times,
                                                "name": agent_dict[player["CharacterID"].lower()] + " on " + team_string + " team",
                                                "agent": curr_player_stat["agent"],
                                                "time_diff": time.time() - curr_player_stat["epoch"]
                                            })

                        party_icon = ''

                        # set party premade icon
                        for party in partyOBJ:
                            if player["Subject"] in partyOBJ[party]:
                                if party not in partyIcons:
                                    partyIcons.update(
                                        {party: PARTYICONLIST[partyCount]})
                                    # PARTY_ICON
                                    party_icon = PARTYICONLIST[partyCount]
                                    partyCount += 1
                                else:
                                    # PARTY_ICON
                                    party_icon = partyIcons[party]
                        playerRank = rank.get_rank(player["Subject"], seasonID)
                        if player["Subject"] == req.puuid:
                            if cfg.get_feature_flag("discord_rpc"):
                                rpc.set_data({"rank": playerRank["rank"], "rank_name": colors.escape_ansi(
                                    NUMBERTORANKS[playerRank["rank"]]) + " | " + str(playerRank["rr"]) + "rr"})

                        ppstats = pstats.get_stats(player["Subject"])
                        hs = ppstats["hs"]
                        kd = ppstats["kd"]

                        player_level = player["PlayerIdentity"].get(
                            "AccountLevel")

                        if player["PlayerIdentity"]["Incognito"]:
                            Namecolor = colors.get_color_from_team(player["TeamID"],
                                                                   names[player["Subject"]],
                                                                   player["Subject"], req.puuid, agent=player["CharacterID"], party_members=partyMembersList)
                        else:
                            Namecolor = colors.get_color_from_team(player["TeamID"],
                                                                   names[player["Subject"]],
                                                                   player["Subject"], req.puuid, party_members=partyMembersList)
                        if lastTeam != player["TeamID"]:
                            if lastTeamBoolean:
                                table.add_empty_row()
                        lastTeam = player['TeamID']
                        lastTeamBoolean = True
                        if player["PlayerIdentity"]["HideAccountLevel"]:
                            if player["Subject"] == req.puuid or player["Subject"] in partyMembersList or hide_levels == False:
                                PLcolor = colors.level_to_color(player_level)
                            else:
                                PLcolor = ""
                        else:
                            PLcolor = colors.level_to_color(player_level)
                        # AGENT
                        agent = colors.get_agent_from_uuid(
                            player["CharacterID"].lower())
                        if agent == "" and len(Players) == 1:
                            isRange = True

                        # NAME
                        name = Namecolor

                        # VIEWS
                        # views = get_views(names[player["Subject"]])

                        # skin
                        skin = loadouts[player["Subject"]]

                        # RANK
                        rankName = NUMBERTORANKS[playerRank["rank"]]

                        # RANK RATING
                        rr = playerRank["rr"]

                        # short peak rank string
                        peakRankAct = f" (e{playerRank['peakrankep']}a{playerRank['peakrankact']})"
                        if not cfg.get_feature_flag("peak_rank_act"):
                            peakRankAct = ""

                        # PEAK RANK
                        peakRank = NUMBERTORANKS[playerRank["peakrank"]
                                                 ] + peakRankAct

                        # LEADERBOARD
                        leaderboard = playerRank["leaderboard"]

                        hs = colors.get_hs_gradient(hs)
                        wr = colors.get_wr_gradient(
                            playerRank["wr"]) + f" ({playerRank['numberofgames']})"

                        if(int(leaderboard) > 0):
                            is_leaderboard_needed = True

                        # LEVEL
                        level = PLcolor

                        players[player["Subject"]]["name"] = name
                        players[player["Subject"]]["agent"] = agent
                        players[player["Subject"]]["rankName"] = rankName
                        players[player["Subject"]]["rr"] = rr
                        players[player["Subject"]]["peak"] = peakRank
                        players[player["Subject"]]["hs"] = hs
                        players[player["Subject"]]["kd"] = kd
                        players[player["Subject"]]["level"] = [
                            player_level, PLcolor]
                        players[player["Subject"]]["wr"] = wr
                        players[player["Subject"]]["leaderboard"] = leaderboard

                        stats.save_data(
                            {
                                player["Subject"]: {
                                    "name": names[player["Subject"]],
                                    "agent": agent_dict[player["CharacterID"].lower()],
                                    "map": map_dict.get(coregame_stats["MapID"].lower()),
                                    "rank": playerRank["rank"],
                                    "rr": rr,
                                    "match_id": coregame.match_id,
                                    "epoch": time.time(),
                                }
                            }
                        )
                        # bar()
                if game_state == "MENUS":
                    already_played_with = []
                    Players = menu.get_party_members(req.puuid, presence)
                    names = namesClass.get_names_from_puuids(Players)
                    playersLoaded = 1
                    Players.sort(key=lambda Players: Players["PlayerIdentity"].get(
                        "AccountLevel"), reverse=True)
                    seen = []
                    for player in Players:
                        if player['Subject'] in loaded_players:
                            continue
                        update_loading_player_count(
                            [playersLoaded, len(Players)])
                        if player not in seen:
                            playersLoaded += 1
                            party_icon = PARTYICONLIST[0]
                            playerRank = rank.get_rank(
                                player["Subject"], seasonID)
                            if player["Subject"] == req.puuid:
                                if cfg.get_feature_flag("discord_rpc"):
                                    rpc.set_data(
                                        {"rank": playerRank["rank"], "rank_name": NUMBERTORANKS[playerRank["rank"]][0] + " | " + str(playerRank["rr"]) + "rr"})
                        ppstats = pstats.get_stats(player["Subject"])
                        hs = ppstats["hs"]
                        kd = colors.get_kd_gradient(ppstats["kd"])

                        player_level = player["PlayerIdentity"].get(
                            "AccountLevel")
                        PLcolor = colors.level_to_color(player_level)

                        # AGENT
                        agent = ""

                        # NAME
                        name = names[player["Subject"]]

                        # RANK
                        rankName = NUMBERTORANKS[playerRank["rank"]]

                        # RANK RATING
                        rr = playerRank["rr"]

                        # short peak rank string
                        peakRankAct = f" (e{playerRank['peakrankep']}a{playerRank['peakrankact']})"
                        if not cfg.get_feature_flag("peak_rank_act"):
                            peakRankAct = ""

                        # PEAK RANK
                        peakRank = [NUMBERTORANKS[playerRank["peakrank"]
                                                  ], peakRankAct]

                        # LEADERBOARD
                        leaderboard = playerRank["leaderboard"]

                        hs = colors.get_hs_gradient(hs)
                        wr = [colors.get_wr_gradient(
                            playerRank["wr"]), f" ({playerRank['numberofgames']})"]

                        if(int(leaderboard) > 0):
                            is_leaderboard_needed = True

                        # LEVEL
                        level = PLcolor

                        draw_player(dict(puuid=player['Subject'], name=name, agent=agent, rankName=rankName, rr=rr, peak=peakRank,
                                         hs=hs, kd=kd, wr=wr, leaderboard=leaderboard, level=[player_level, PLcolor]), [playersLoaded, len(Players)])

                        loaded_players.append(player['Subject'])

                        seen.append(player["Subject"])
                time.sleep(1)
                if kill_threads:
                    break
        except Exception as e:
            main_ui.deactivate()
            traceback.print_exc()

    loading_status.set_text("Finishing up")
    loading_ui.draw()

    threads.append(threading.Thread(target=update_rpc,
                                    name="update_rpc", args=(), daemon=True))

    threads.append(threading.Thread(
        target=game_state_loop, name="game_state_loop", args=(), daemon=True))

    def killWithValorant():
        nonlocal kill_threads
        while True:
            if "VALORANT.exe" not in (i.name() for i in psutil.process_iter()):
                kill_threads = True
                main_ui.deactivate()
                os._exit(0)

    threads.append(threading.Thread(
        target=killWithValorant, args=(), daemon=True))

    for thread in threads:
        thread.start()

    main_ui.activate()


if __name__ == '__main__':
    curses.wrapper(main)
