import curses
import asyncio
import random
import time
import sys
import os
import requests
import urllib3
import threading
from TermUI.button import Button
from TermUI.ui import UI
from TermUI.region import Region
from TermUI.position import Position
from TermUI.text import Text
from TermUI.region import BoxCharacters
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

from TermUI.button import Button

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

    loaded = False

    def activate_loading():
        loading_ui.activate()

    def deactivate_loading():
        while True:
            if loaded:
                loading_ui.deactivate()
                break

    threading.Thread(target=activate_loading, name="loading",
                     args=(), daemon=True).start()
    threading.Thread(target=deactivate_loading, name="deloading",
                     args=(), daemon=True).start()

    main_ui = UI(stdscr)

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

    def scoreboard_tab(button):
        disable_all_tabs()
        content_regions.get("scoreboard").visible = True
        highlight_button(button)

    def skins_tab(button):
        disable_all_tabs()
        content_regions.get("skins").visible = True
        highlight_button(button)

    def chat_tab(button):
        disable_all_tabs()
        content_regions.get("chat").visible = True
        highlight_button(button)

    tab_offset = Position(-1, -1)
    pretabs = {
        "Scoreboard": scoreboard_tab,
        "Skins": skins_tab,
        "Chat": chat_tab
    }
    tabs = []
    for name in pretabs:
        created = Button(name, tab_offset, pretabs[name])
        created.rounded = True
        tabs.append(created)
        tab_region.add_element(created)
        tab_offset += Position(created.size.x + 1, 0)

    tabs[0].color = HIGHLIGHTED_TAB

    content_regions = {
        "scoreboard": Region(
            "", Position(0, 2), Position(119, 29)),
        "skins": Region(
            "", Position(0, 2), Position(119, 29)),
        "chat": Region(
            "", Position(0, 2), Position(119, 29))
    }

    for region in content_regions:
        main_ui.add_region(content_regions.get(region))

    disable_all_tabs()

    content_regions['scoreboard'].visible = True

    content_regions.get("scoreboard").add_element(
        Text("Scoreboard", Position(0, 0)))
    content_regions.get("skins").add_element(
        Text("Skins", Position(0, 0)))
    content_regions.get("chat").add_element(
        Text("Chat", Position(0, 0)))

    team_1 = random.shuffle(["Skye", "Sova", "Omen", "Raze", "Reyna"])
    team_2 = random.shuffle(["Skye", "Sova", "Omen", "Raze", "Reyna"])

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

    # print(color("\nVisit https://vry.netlify.app/matchLoadouts to view full player inventories\n", fore=(255, 253, 205)))
    # chatlog(color("\nVisit https://vry.netlify.app/matchLoadouts to view full player inventories\n", fore=(255, 253, 205)))

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
            rpc_status.set_text("● RPC Running")
            rpc_status.color = SUCCESS_GREEN
            rpc_status.start = Position(content_regions.get(
                "scoreboard").size.x-2-len(rpc_status.text), 3)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            game_state = loop.run_until_complete(
                Wss.recconect_to_websocket(game_state))
            log(f"new game state: {game_state}")
            loop.close()
            if kill_threads:
                break

    def redraw():
        "Threaded method to redraw screen once every 5 seconds."
        while True:
            main_ui.draw()
            time.sleep(5)
            if kill_threads:
                break

    def game_state_loop():
        nonlocal rpc
        nonlocal game_state
        log(f"getting new {game_state} scoreboard")
        lastGameState = game_state
        game_state_dict = {
            "INGAME": 'In-Game',
            "PREGAME": 'Agent Select',
            "MENUS": 'In-Menus',
        }

        is_leaderboard_needed = False
        while True:
            if game_state == "MENUS":
                already_played_with = []
                Players = menu.get_party_members(req.puuid, presence)
                names = namesClass.get_names_from_puuids(Players)
                playersLoaded = 1
                Players.sort(key=lambda Players: Players["PlayerIdentity"].get(
                    "AccountLevel"), reverse=True)
                seen = []
                for player in Players:

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
                    kd = ppstats["kd"]

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

                    seen.append(player["Subject"])
            time.sleep(1)
            if kill_threads:
                break

    threads.append(threading.Thread(target=update_rpc,
                                    name="update_rpc", args=(), daemon=True))

    threads.append(threading.Thread(
        target=redraw, name="redraw", args=(), daemon=True))

    threads.append(threading.Thread(
        target=game_state_loop, name="game_state_loop", args=(), daemon=True))

    for thread in threads:
        thread.start()

    loaded = True
    main_ui.activate()


if __name__ == '__main__':
    curses.wrapper(main)
