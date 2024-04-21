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
    # Color pairs. name, FG, BG
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Menu title
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) # Correct text
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) # Incorrect text

def display_title(stdscr):
    # Top title
    stdscr.addstr(0, 0, " " * width, curses.color_pair(1))
    stdscr.addstr(0, width // 2 - len("TYPE NINJA") // 2, "TYPE NINJA", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(0, width - len("by torshin5ergey"), "by torshin5ergey", curses.color_pair(1))

# Bottom bar
def display_controls(stdscr):
    # X Exit
    stdscr.addstr(height-1, 0, "^X", curses.color_pair(1))
    stdscr.addstr(" Exit")
    # R Start
    stdscr.addstr(height-1, 10, "^R", curses.color_pair(1))
    stdscr.addstr(" Start")

def display_stats(stdscr):
    #stdscr.addstr(height-1, 0, "Q", curses.color_pair(1))
    # TODO: wpm
    # TODO: acc
    # TODO: time
    pass

def display_game(stdscr, user:str, typed_words:list[str], to_type_words:list[str]):
    typed = " ".join(typed_words)
    to_type = " ".join(to_type_words)
    # Display dim typed text
    dim_string_length = (width // 2) - len(typed) - len(user) - 1
    stdscr.addstr(4, max(0, dim_string_length), typed[max(0, -dim_string_length):],curses.color_pair(2) | curses.A_DIM)
    # Display text to type
    stdscr.addstr(4, width // 2 - len(user), to_type[:width//2+len(user)])

    pass

def display_user_input(stdscr, user_input:str):
    stdscr.move(5, width // 2)
    stdscr.addstr(5, (width // 2) - len(user_input), user_input)

def display_time():
    pass