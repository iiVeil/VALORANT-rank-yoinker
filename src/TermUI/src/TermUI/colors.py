import curses

"""Running this file will give you a clean output of the color codes used in the TermUI library
"""


def main(stdscr):
    stdscr.nodelay(True)
    stdscr.keypad(1)
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        if i < 255:
            curses.init_pair(i + 1, i, -1)
    for i in range(0, 255):
        stdscr.addstr(str(i) + " ", curses.color_pair(i))
    while True:
        if stdscr.getch() == ord("q"):
            return


if __name__ == "__main__":
    curses.wrapper(main)
