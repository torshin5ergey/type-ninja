# CLI
import curses
import time

'''
x = width // 2 - len("Hello, world!") // 2
y = height // 2
stdscr.addstr(y, x, "Hello, world!")
'''
table_width = 55

def init_colorpairs(stdscr):
    # Color pairs. name, FG, BG
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Menu title
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) # Correct text
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK) # Incorrect text

def get_window_size(stdscr):
    # Get window size
    global height, width
    height, width = stdscr.getmaxyx()
    return height, width

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

# wpm, c_accuracy, w_accuracy, w_incorrect, time
def display_stats(stdscr, wpm:int, ch_acc:float, c_inc:int, w_acc:float, w_inc:int) -> None:
    str_wpm = str(wpm).rjust(3)
    str_ch_acc = str(ch_acc).rjust(5)
    stdscr.addstr(7, width//2 - table_width//2, f"|                        wpm  {str_wpm}                     |", curses.A_BOLD)
    stdscr.addstr(8, width//2 - table_width//2, "|-----------------------------------------------------|")
    stdscr.addstr(9, width//2 - table_width//2, f"|   char accuracy | {str_ch_acc}% |    word accuracy| {str(w_acc).rjust(5)}% |")
    stdscr.addstr(10, width//2 - table_width//2, f"| incorrect chars | {str(c_inc).rjust(5)}  | incorrect words | {str(w_inc).rjust(5)}  |")

    # TODO: wpm
    # TODO: acc
    # TODO: time
    pass

def display_task(stdscr, user:str, user_typed:list[str], task_typed:list[str], task_to_type:list[str]) -> None:
    typed = " ".join(user_typed)
    to_type = " ".join(task_to_type)
    # Display dim typed text
    dim_length = (width // 2) - len(typed) - len(user) - 1
    
    stdscr.addstr(4, max(0, dim_length), typed[max(0, -dim_length):], curses.A_DIM | curses.color_pair(2))
    '''
    cursor = dim_length
    for i, v in enumerate(user_typed):
        color = curses.color_pair(2) if v == task_typed[i] else curses.color_pair(3)
        stdscr.addstr(4, max(0, cursor), typed[max(0, -cursor):], curses.A_DIM | color)
        cursor += len(v) + 1
    '''

    # Display text to type
    right = min(width, width//2+len(user)) # Right slice border
    stdscr.addstr(4, max(0, width // 2 - len(user)), to_type[:right])
    pass

def display_user_input(stdscr, user:str, correct:bool):
    # Set text color depends on the correctness
    color = curses.color_pair(3) if not correct else 0
    left = max(0, -((width // 2)-len(user))) # Left print slice start
    stdscr.addstr(5, max(0, (width // 2) - len(user)), user[left:], color)
    stdscr.move(5, width // 2)

def display_time(stdscr, time:float):
    time = str(time).rjust(2)
    stdscr.addstr(2, (width // 2) - len(time)//2, time)
    stdscr.move(5, width // 2)
    stdscr.refresh()
    pass