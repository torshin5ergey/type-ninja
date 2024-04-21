import curses
import time
import ui
import text_generator

def get_user_iunput(stdscr, user_input:str):
    #global typed, to_type
    curses.cbreak()
    char = stdscr.getch()
    if char == curses.KEY_BACKSPACE or char == 8: # backspace
        if len(user_input) > 0:
            user_input = user_input[:-1]
    elif char == 32: # space
        typed.append(user_input)
        del text[0]
        return ''
    else:
        user_input += chr(char)
    return user_input

def is_correct_input(user, task) -> bool:
    if user == task[:len(user)]:
        return True
    else:
        return False

def main(stdscr):
    global typed, text, is_correct
    # curses.curs_set(0)
    stdscr.clear()
    curses.curs_set(False)
    curses.start_color()
    # Menu
    ui.get_window_size(stdscr)
    ui.display_title(stdscr)
    ui.display_controls(stdscr)

    stdscr.refresh()

    # Main menu loop
    while True:
        key = stdscr.getch()
        if key == 24:
            break
        elif key == 18:
            text = text_generator.get_random_word()

            curses.curs_set(True)
            curses.echo()
    
            typed = [] # Typed words (after space)
            user_input = '' # Current typed word
            is_correct = True

            while True:
                    stdscr.clear()
                    ui.display_title(stdscr)
                    ui.display_task(stdscr, user_input, typed, text)
                    ui.display_user_input(stdscr, user_input, is_correct)
                    user_input = get_user_iunput(stdscr, user_input)
                    is_correct = is_correct_input(user_input, text[0])
                    stdscr.refresh()
                    start_time = time.time()
            curses.noecho()


curses.wrapper(main)