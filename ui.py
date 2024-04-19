# CLI
import curses

'''
x = width // 2 - len("Hello, world!") // 2
y = height // 2
stdscr.addstr(y, x, "Hello, world!")
'''

def get_window_size(stdscr):
    # Get window size
    global height, width
    height, width = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

def display_menu(stdscr):
    # Top title
    stdscr.addstr(0, 0, " " * width, curses.color_pair(1))
    stdscr.addstr(0, width // 2 - len("TYPE NINJA") // 2, "TYPE NINJA", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(0, width - len("by torshin5ergey"), "by torshin5ergey", curses.color_pair(1))

    # Bottom bar
    # Q Quit
    stdscr.addstr(height-1, 0, "^X", curses.color_pair(1))
    stdscr.addstr(" Exit")
    # S Start
    stdscr.addstr(height-1, 10, "^R", curses.color_pair(1))
    stdscr.addstr(" Start")

def display_stats(stdscr):
    #stdscr.addstr(height-1, 0, "Q", curses.color_pair(1))
    # TODO: wpm
    # TODO: acc
    # TODO: time
    pass

def display_time():
    pass