import curses
import time
import string as strings
from enum import Enum
from .position import Position
from .element import Element


class Textbox(Element):
    BACKSPACE = (curses.KEY_BACKSPACE, 8, 127)
    ENTER = (curses.KEY_ENTER, 36, 10, 13)

    def __init__(self, placeholder: str, position: Position, size: Position):
        super().__init__(position)
        self.placeholder = placeholder
        self.placeholder_active = True
        self.size = ((size) - Position(1, 1)) + Position(0, 3)
        self.pack = {
            "up": Position(position.x, position.y-1),
            "down": Position(position.x, position.y+self.size.y+1),
            "right": Position(
                self.size.x+position.x+1, position.y)}
        self.callback = 1
        self.on_enter = None
        self.on_input = None
        self.placeholder_color = 243
        self.maxchars = self.size.x - 4
        self.char_limit = 0
        self.password = False
        self.text = ""
        self.display = self.text

    def reset(self):
        """Reset the text in the texbox, display and content
        """
        self.text = ""

    def draw(self) -> None:
        """Draws the textbox to the screen

        This will do nothing if you do not add it to a region using Region.add_region().
        """
        if self.password:
            new = ""
            for char in self.display:
                new += "*"
            self.display = new
        else:
            self.display = self.text

        if self.region is None or self.hidden:
            return
        # * Initialize the corners of the textbox
        self.addstr(self.start.y, self.start.x,
                    TextBoxCharacters.TOPLEFT.value, curses.color_pair(self.color))
        self.addstr(self.start.y, self.end.x,
                    TextBoxCharacters.TOPRIGHT.value, curses.color_pair(self.color))
        self.addstr(self.end.y, self.start.x,
                    TextBoxCharacters.BOTTOMLEFT.value, curses.color_pair(self.color))
        self.addstr(self.end.y, self.end.x,
                    TextBoxCharacters.BOTTOMRIGHT.value, curses.color_pair(self.color))

        # * Vertical lines
        for iy in range(self.end.y-self.start.y):
            if 0 < iy < self.end.y:
                self.addstr(iy+self.start.y, self.start.x,
                            TextBoxCharacters.VERTICAL.value, curses.color_pair(self.color))
                self.addstr(
                    iy+self.start.y, self.end.x,
                    TextBoxCharacters.VERTICAL.value, curses.color_pair(self.color))

        # * Horizontal lines
        for ix in range(self.end.x-self.start.x):
            if 0 < ix < self.end.x:
                char = TextBoxCharacters.HORIZONTAL.value
                self.addstr(self.start.y, ix+self.start.x,
                            char, curses.color_pair(self.color))
                self.addstr(
                    self.end.y, ix+self.start.x,
                    TextBoxCharacters.HORIZONTAL.value, curses.color_pair(self.color))
        if self.text == "":
            self.addstr(
                self.start.y+1, self.start.x+2, self.placeholder, curses.color_pair(self.placeholder_color))
        else:
            text = self.display
            if len(text) > self.maxchars:
                text = ".." + self.display[::-1][:self.maxchars-1][::-1]
            self.addstr(
                self.start.y+1, self.start.x+2, text, curses.color_pair(self.color))

    def click(self):
        """Focus the textbox and allow the user to type

        This will do nothing if you do not add it to a region using Region.add_region().
        """
        if self.region is None or self.hidden:
            return
        cursor = len(self.text) + \
            1 if len(self.text) <= self.maxchars else self.maxchars+2
        self.region.ui.window.move(
            self.start.y+1, cursor+self.start.x+1)
        curses.curs_set(1)
        for string in self.__get_user_input(string=self.text, cursor=cursor):
            self.text, self.display = string["content"], string["display"]

            self.addstr(self.start.y+1, self.start.x + 2,
                        self.display, self.color)
            if string["cursor"] > 0:
                self.region.ui.window.move(
                    self.start.y+1, string["cursor"]+self.start.x+1)
            else:
                curses.curs_set(0)
            self.region.ui.draw()

    def __get_user_input(self, string: str = '', cursor: int = 0):
        """A generator for getting user input and compiling it to a string. backspace, enter, and lost focus on click supported

        Args:
            string (str, optional): The string to start the generator with. Defaults to ''.
            cursor (int, optional): The starting cursor position in the textbox. Defaults to 0.

        Yields:
            dict:
                "display" > str: the text to store in the textbox
                "content" > str: the content to display in the textbox
                "cursor" > int: the cursor position
        """
        currtime = time.time()*1000
        while True:
            if time.time()*1000 - currtime < 300:
                continue
            self.region.ui.window.move(
                self.start.y+1, cursor+self.start.x+1)
            key = self.region.ui.window.getch()
            if key in Textbox.ENTER:
                yield {"display": ''.join(["*" for _ in string]) if self.password else string, "cursor": -1, "content": string}
                if self.on_enter is not None:
                    self.on_enter(self)
                return
            elif key == curses.KEY_DC:
                if len(string) > 0:
                    string = ""
                    cursor = 1
                    yield {"display": string, "cursor": cursor, "content": string}
            elif key in Textbox.BACKSPACE:
                if len(string) > 0:
                    string = string[:-1]
                    cursor = len(string)+1
                    data = {"display": ''.join(
                        ["*" for _ in string]) if self.password else string, "cursor": cursor, "content": string}
                    if len(string) > self.maxchars:
                        cursor = self.maxchars+2

                    yield data
            elif key == curses.KEY_MOUSE:
                _, mx, my, _, _ = curses.getmouse()
                position = Position(mx, my)
                if not self.in_bounds(position):
                    curses.curs_set(0)
                    yield {"display": ''.join(["*" for _ in string]) if self.password else string, "cursor": -1, "content": string}
                    self.region.ui.get_clickable(position)
                    return
            else:
                if chr(key) in strings.ascii_letters + strings.punctuation + strings.digits + " ":
                    if self.char_limit > 0 and len(string) >= self.char_limit:
                        continue
                    string += chr(key)
                    cursor += 1
                    data = {"display": ''.join(
                        ["*" for _ in string]) if self.password else string, "cursor": cursor, "content": string}
                    if len(string) > self.maxchars:
                        cursor = self.maxchars+2
                    if self.on_input is not None:
                        self.on_input(chr(key))
                    yield data


class TextBoxCharacters(Enum):
    TOPLEFT = "╒"
    TOPRIGHT = "╕"
    BOTTOMLEFT = "╘"
    BOTTOMRIGHT = "╛"
    HORIZONTAL = "═"
    VERTICAL = "│"
