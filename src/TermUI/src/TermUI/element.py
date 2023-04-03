from .position import Position


class Element:
    """
    ? Description
    * * An element that exists within a region
    """

    def __init__(self, start: Position):
        self.region = None  # the region it resides in
        self.start = start
        self.hidden = False
        self.end = None
        self.color = -1
        self.callback = None
        self.data = {}

    def in_bounds(self, position: Position) -> bool:
        """Checks if a position is in bounds

        Args:
            position (Position): the position to check
        """

        x, y = position.x, position.y

        def in_x_bound():
            return self.start.x <= x <= self.end.x

        def in_y_bound():
            return self.start.y <= y <= self.end.y

        return in_x_bound() and in_y_bound()

    def addstr(self, y: int, x: int, string: str, options=0):
        """Shorthand helper function to add a string to the screen

        Args:
            y (int): Row value
            x (int): Column value
            string (str): The string to add
            options (int, optional): Other options: color, formatting, etc. Defaults to 0.
        """
        self.region.ui.window.addstr(y, x, string, options)
