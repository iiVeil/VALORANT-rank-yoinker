from TermUI.position import Position
from TermUI.text import Text
from TermUI.region import Region
from TermUI.ui import UI


class Scoreboard:

    def __init__(self, height: int, width: int, start: Position, region: UI):
        self.teams = {
            "ally": {
                "uuid": []
            },
            "enemy": {
                "uuid": []
            }
        }
        # rank is just colored num, radiant is lb position. 6 spaces ( #500 ) ( P1 )
        # name is clickable text to open more stats & tag. 18 spaces (16 max + 2 padding)
        # HS. 5 spaces ( 100 )
        # WR (Games). 13 spaces ( 100% (9999) )
        # Level. 6 spaces ( 9999 )
        # 48 spaces total
        self.size = Position(width, height)
        self.parent = region
        self.region = Region("", start, self.size)
        self.rows = 6
        self.ally_columns = [["Rank", 5], ["Agent", 11], ["Name", 18], [
            "HS", 5], ["Level", 6]]
        self.enemy_columns = self.ally_columns[::-1]
        self.columns = self.ally_columns + [['Party', 1]] + self.enemy_columns

    def draw(self):
        chars = Scoreboard.Characters
        height = self.size.y
        width = self.size.x
        row_offset = 2
        for _ in range(self.rows):
            self.region.add_element(Text(
                ''.join(([chars.LeftIntersection] + [chars.Horizontal *
                                                     (width-2)] + [chars.RightIntersection])),
                Position(-1, row_offset)
            ))
            row_offset += 3

        self.parent.add_region(self.region)

    def fill_table(self):
        # ally
        base_offset = Position(1, 1)
        for i, player in enumerate(self.teams.get("ally")):
            offset = base_offset + Position(0, i*3)
            data = self.teams.get("ally").get(player)
            for element in data:
                if isinstance(element, list):
                    ele = Text(data[0][0], Position(offset))

                    ele.color = data[0][1]

            self.region.add_element(rank)

    class Characters:
        LeftIntersection = "├"
        RightIntersection = "┤"
        TopIntersection = "┬"
        BottomIntersection = "┴"
        FourWayIntersection = "┼"
        Vertical = "│"
        Horizontal = "─"
        TopLeft = "╭"
        TopRight = "╮"
        BottomLeft = "╰"
        BottomRight = "╯"
