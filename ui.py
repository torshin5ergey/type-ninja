# CLI
import curses
import time

'''
x = width // 2 - len("Hello, world!") // 2
y = height // 2
stdscr.addstr(y, x, "Hello, world!")
'''
STATS_TABLE_W = 55 # Stats table width
EXIT_SHORTCUT = "^X"
START_SHORTCUT = "^R"

def init_colorpairs(stdscr) -> None:
    # Color pairs. name, FG, BG
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Menu title
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) # Correct text
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) # Incorrect text

def get_window_size(stdscr) -> tuple:
    # Get window size
    global height, width
    height, width = stdscr.getmaxyx() # Screen width, height
    return height, width

def display_title(stdscr):
    # Top title
    stdscr.addstr(0, 0, " " * width, curses.color_pair(1))
    stdscr.addstr(0, width // 2 - len("TYPE NINJA") // 2, "TYPE NINJA", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(0, width - len("by torshin5ergey"), "by torshin5ergey", curses.color_pair(1))

# Bottom bar
def display_controls(stdscr):
    # X Exit
    stdscr.addstr(height-1, 0, EXIT_SHORTCUT, curses.color_pair(1))
    stdscr.addstr(" Exit")
    # R Start
    stdscr.addstr(height-1, 10, START_SHORTCUT, curses.color_pair(1))
    stdscr.addstr(" Start")

# wpm, c_accuracy, w_accuracy, w_incorrect, time
def display_stats(stdscr, wpm:int, ch_acc:float, c_inc:int, w_acc:float, w_inc:int) -> None:
    wpm = str(wpm).rjust(3)
    ch_acc = str(ch_acc).rjust(5)
    w_acc = str(w_acc).rjust(5)
    c_inc = str(c_inc).rjust(5)
    w_inc = str(w_inc).rjust(5)
    # Table header
    stats_header = f"|{' ' * (STATS_TABLE_W//2-4)}wpm {wpm}{' ' * (STATS_TABLE_W//2-4)}|"
    stdscr.addstr(7, width//2 - STATS_TABLE_W//2, stats_header, curses.A_BOLD)
    # Table body
    stdscr.addstr(8, width//2 - STATS_TABLE_W//2, f"|{'-' * (STATS_TABLE_W-2)}|")
    stdscr.addstr(9, width//2 - STATS_TABLE_W//2, f"|   char accuracy | {ch_acc}% |    word accuracy| {w_acc}% |")
    stdscr.addstr(10, width//2 - STATS_TABLE_W//2, f"| incorrect chars | {c_inc}  | incorrect words | {w_inc}  |")

def display_task(stdscr, user:str, user_typed:list[str], task_typed:list[str], task_to_type:list[str]) -> None:
    typed = " ".join(user_typed)
    to_type = " ".join(task_to_type)

    # Display dim typed text
    dim_length = (width // 2) - len(typed) - len(user) - 1
    stdscr.addstr(4, max(0, dim_length), typed[max(0, -dim_length):], curses.A_DIM | curses.color_pair(2))

    # Display text to type
    right = min(width, width//2+len(user)) # Right slice border
    stdscr.addstr(4, max(0, width // 2 - len(user)), to_type[:right])

def display_user_input(stdscr, user:str, correct:bool) -> None:
    # Set text color depends on the correctness
    color = curses.color_pair(3) if not correct else 0
    left = max(0, -((width // 2)-len(user))) # Left print slice start
    stdscr.addstr(5, max(0, (width // 2) - len(user)), user[left:], color)
    stdscr.move(5, width // 2)

def display_time(stdscr, time:float) -> None:
    time = str(time).rjust(2)
    stdscr.addstr(2, (width // 2) - len(time)//2, time)
    stdscr.move(5, width // 2)
    stdscr.refresh()
