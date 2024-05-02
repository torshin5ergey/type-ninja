import time
import threading
import curses
import ui
import text_generator

KEY_EXIT = 24 # ^X exit
KEY_START = 18 # ^R start
KEY_HELP = 263 # ^H help
KEY_ENTER = 10 # enter
KEY_BACKSPACE_UNX = 127 # backspace
KEY_BACKSPACE_WND = 8 # backspace
KEY_SPACE = 32 # space

# Exception class for exiting started test
class EndTestException(Exception):
    def __init__(self, message=''):
        self.message = message
        super().__init__(self.message)

def get_user_input(stdscr, user_input:str, user_typed:list[str], task:list[str], task_typed:list[str]) -> tuple:
    curses.cbreak()
    char = stdscr.getch()
    if char == KEY_ENTER:
        raise EndTestException
    elif (char == curses.KEY_BACKSPACE or char == KEY_BACKSPACE_UNX or char == KEY_BACKSPACE_WND):
        if len(user_input) == 0:
            user_input = ''
        else:
            user_input = user_input[:-1]
    elif char == KEY_SPACE:
        user_typed.append(user_input)
        task_typed.append(task.pop(0))
        user_input = ''
    else:
        try:
            user_input += chr(char)
        except ValueError:
            return '', task, task_typed
    return user_input, task, task_typed

def is_correct_input(user_input:str, task) -> bool:
    if user_input == task[:len(user_input)]:
        return True
    else:
        return False

def time_counter(stdscr, width, height, start:float) -> None:
    global remaining, stop_flag
    while not stop_flag:
        remaining = round(timer - (time.time() - start))
        if remaining < 0:
            break
        ui.display_time(stdscr, width, height, remaining)
        time.sleep(.1)

def calculate_stats(typed_words:list[str], task:list[str], remaining:int) -> tuple:
    # User typed words stats
    typed_words_count = len(typed_words)
    typed_chars = len(" ".join(typed_words))
    # Task words stats
    task_chars = len(" ".join(task))
    # Calculate WPM (words per minute)
    try:
        wpm = round(typed_words_count / ((timer - remaining) / 60))
    except ZeroDivisionError:
        wpm = 0
    # Calculate incorrect words count
    words_incorrect = sum(1 for w1, w2 in zip(task, typed_words) if w1 != w2)
    # Calcuate correect words percentage
    try:
        words_accuracy = round(((typed_chars - words_incorrect) / typed_chars) * 100, 2)
    except ZeroDivisionError:
        words_accuracy = 0
    # Calculate correct chars percentage
    total_correct_chars = 0
    total_incorrect_chars = 0
    for w1, w2 in zip(task, typed_words):
        # Length of minimal length word
        min_len = min(len(w1), len(w2))
        # Count correct chars
        correct_chars = sum(1 for c1, c2 in zip(w1[:min_len], w2[:min_len]) if c1 == c2)
        # Count incorrect chars
        incorrect_chars = max(len(w1), len(w2)) - correct_chars
        total_correct_chars += correct_chars
        total_incorrect_chars += incorrect_chars
    total_chars = sum(max(len(w1), len(w2)) for w1, w2 in zip(task, typed_words))
    try:
        char_accuracy = round((total_correct_chars / total_chars) * 100, 2)
    except ZeroDivisionError:
        char_accuracy = 0
    return wpm, char_accuracy, total_incorrect_chars, words_accuracy, words_incorrect

def main(stdscr):
    global timer, remaining, stop_flag
    # Main menu loop
    while True:
            stdscr.clear()
            curses.curs_set(False)
            curses.noecho()
            curses.start_color()
            ui.init_colorpairs(stdscr)
            # Menu
            width, height = ui.get_window_size(stdscr)
            ui.display_title(stdscr, width, height)
            ui.display_mainscreen(stdscr, width, height)
            ui.display_controls(stdscr, width, height, 'default')
            stdscr.refresh()

            key = stdscr.getch()
            if key == KEY_EXIT:
                break
            elif key == KEY_HELP:
                stdscr.clear()
                ui.display_title(stdscr, width, height)
                ui.display_help(stdscr, width, height)
                ui.display_controls(stdscr, width, height, 'enter')
                while True:
                    key = stdscr.getch()
                    if key == KEY_ENTER:
                        break
            elif key == KEY_START:
                stdscr.clear()
                text = text_generator.get_random_word()

                curses.curs_set(True)
                curses.echo()
                user_typed = [] # Typed words (after space)
                task_typed = [] # Original words, that user done
                user_input = '' # Current typed word
                is_correct = True # Is correct current word
                remaining = 0 # Time remaining
                timer = 60 # Sec

                # TODO: Type to start

                start_time = time.time()

                # Start time display thread
                stop_flag = False
                time_thread = threading.Thread(target=time_counter, args=(stdscr, width, height, start_time), daemon=True)
                time_thread.start()

                stdscr.refresh()
                while time_thread.is_alive():
                    stdscr.clear()
                    width, height = ui.get_window_size(stdscr)
                    ui.display_title(stdscr, width, height)
                    ui.display_controls(stdscr, width, height, 'enter')
                    wpm, ch_accuracy, ch_incorrect, word_accuracy, words_incorrect = calculate_stats(user_typed, task_typed, remaining)
                    ui.display_stats(stdscr, width, height, wpm, ch_accuracy, ch_incorrect, word_accuracy, words_incorrect)
                    ui.display_task(stdscr, width, height, user_input, user_typed, task_typed, text)
                    ui.display_user_input(stdscr, width, height, user_input, is_correct)
                    stdscr.refresh()
                    try:
                        user_input, text, task_typed = get_user_input(stdscr, user_input, user_typed, text, task_typed)
                    except EndTestException:
                        stop_flag = True
                        break
                    is_correct = is_correct_input(user_input, text[0])
                
                if not stop_flag:
                    key = stdscr.getch()

curses.wrapper(main)