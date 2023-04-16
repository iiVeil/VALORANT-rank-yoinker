from src.constants import tierDict
import re


class Colors:
    ENEMY_RED = 13
    TEAM_BLUE = 10
    ME_YELLOW = 227
    CYAN = 38
    LIGHT_YELLOW = 228
    BLUE = 27
    ORANGE = 209
    GRAY = 250
    DEFAULT = 232

    def __init__(self, hide_names, agent_dict, AGENTCOLORLIST):
        self.hide_names = hide_names
        self.agent_dict = agent_dict
        self.tier_dict = tierDict
        self.AGENTCOLORLIST = AGENTCOLORLIST

    def get_color_from_team(self, team, name, playerPuuid, selfPuuid, agent=None, party_members=None):
        orig_name = name
        if agent is not None:
            if self.hide_names:
                if agent != "":
                    name = self.agent_dict[agent.lower()]
                else:
                    name = "Player"
        if team == 'Red':
            if playerPuuid not in party_members:
                Teamcolor = Colors.ENEMY_RED
            else:
                Teamcolor = Colors.ENEMY_RED
        elif team == 'Blue':
            if playerPuuid not in party_members:
                Teamcolor = Colors.TEAM_BLUE
            else:
                Teamcolor = Colors.TEAM_BLUE
        else:
            Teamcolor = ''
        if playerPuuid == selfPuuid:
            Teamcolor = Colors.ME_YELLOW
        return Teamcolor

    def get_rgb_color_from_skin(self, skin_id, valoApiSkins):
        for skin in valoApiSkins.json()["data"]:
            if skin_id == skin["uuid"]:
                return self.tier_dict[skin["contentTierUuid"]]

    def level_to_color(self, level):
        if 0 <= level < 100:
            return Colors.GRAY
        elif 100 <= level < 200:
            return Colors.ORANGE
        elif 200 <= level < 300:
            return Colors.BLUE
        elif 300 <= level < 400:
            return Colors.LIGHT_YELLOW
        elif 400 <= level:
            return Colors.CYAN

    def get_agent_from_uuid(self, agentUUID):
        agent = str(self.agent_dict.get(agentUUID))
        color = self.AGENTCOLORLIST.get(agent.lower())

        if color is None:
            color = Colors.DEFAULT

        return [agent, color]

    def get_hs_gradient(self, number):
        try:
            number = int(number)
        except ValueError:
            return ["N/A", 238]

        if 0 < number <= 5:
            return [number, 89]
        elif 5 < number <= 10:
            return [number, 173]
        elif 10 < number <= 20:
            return [number, 149]
        elif 20 < number <= 29:
            return [number, 77]
        elif 29 < number:
            return [f"✦ {number}", 221]

    def get_kd_gradient(self, number):
        if 0 <= number <= .7:
            return [number, 89]
        elif .7 < number <= 1:
            return [number, 173]
        elif 1 < number <= 1.2:
            return [number, 149]
        elif 1.2 < number <= 1.5:
            return [number, 77]
        elif 1.5 < number:
            return [f"✦ {number}", 221]

    def get_wr_gradient(self, number):
        try:
            number = int(number)
        except ValueError:
            return ["N/A", 238]

        if 0 < number <= 15:
            return [number, 89]
        elif 15 < number <= 25:
            return [number, 173]
        elif 25 < number <= 40:
            return [number, 149]
        elif 40 < number <= 60:
            return [number, 77]
        elif 60 < number:
            return [f"✦ {number}", 221]

    def escape_ansi(self, line):
        ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', line)
