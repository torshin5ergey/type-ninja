import curses
import time
import threading
import ui
import text_generator

def get_user_input(stdscr, user_input:str):
    #global typed, to_type
    curses.cbreak()
    char = stdscr.getch()
    if char == curses.KEY_BACKSPACE or char == 127 or char == 8: # backspace
        if len(user_input) > 0:
            user_input = user_input[:-1]
    elif char == 32: # space
        user_typed.append(user_input)
        task_typed.append(text.pop(0))
        return ''
    else:
        user_input += chr(char)
    return user_input

def is_correct_input(user_input:str, task) -> bool:
    if user_input == task[:len(user_input)]:
        return True
    else:
        return False

def time_counter(stdscr, start:float):
    global remaining
    while True:
        remaining = round(timer - (time.time() - start))
        if remaining < 0:
            break
        ui.display_time(stdscr, remaining)
        time.sleep(.01)

def calculate_stats(typed_words:list[str], task:list[str], remaining:int):
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
    global user_typed, text, is_correct, task_typed
    global timer, remaining
    # Main menu loop
    while True:
            # curses.curs_set(0)
            stdscr.clear()
            curses.curs_set(False)
            curses.noecho()
            curses.start_color()
            ui.init_colorpairs(stdscr)
            # Menu
            width, height = ui.get_window_size(stdscr)
            ui.display_title(stdscr)
            ui.display_controls(stdscr)
            stdscr.refresh()
            key = stdscr.getch()
            if key == 24:
                break
            elif key == 18:
                stdscr.clear()
                text = text_generator.get_random_word()

                curses.curs_set(True)
                curses.echo()

                user_typed = [] # Typed words (after space)
                task_typed = [] # Original words, that user done
                user_input = '' # Current typed word
                is_correct = True

                #wpm = 0
                #ch_accuracy = 0
                #word_accuracy = 0
                #words_incorrect = 0 # incorrect typed words counter
                remaining = 0 # time remaining

                timer = 60 # sec

                # Before start
                '''
                ui.display_title(stdscr)
                ui.display_task(stdscr, user_input, user_typed, text)
                stdscr.addstr(2, width, str(timer))
                stdscr.move(5, width)
                stdscr.refresh()
                user_input = chr(stdscr.getch())
                is_correct = is_correct_input(user_input, text[0])
                '''

                start_time = time.time()
                time_thread = threading.Thread(target=time_counter, args=(stdscr, start_time), daemon=True)
                time_thread.start()
                stdscr.refresh()
                while time_thread.is_alive():
                    stdscr.clear()
                    ui.display_title(stdscr)
                    wpm, ch_accuracy, ch_incorrect, word_accuracy, words_incorrect = calculate_stats(user_typed, task_typed, remaining)
                    ui.display_stats(stdscr, wpm, ch_accuracy, ch_incorrect, word_accuracy, words_incorrect)
                    ui.display_task(stdscr, user_input, user_typed, task_typed, text)
                    ui.display_user_input(stdscr, user_input, is_correct)
                    stdscr.refresh()
                    user_input = get_user_input(stdscr, user_input)
                    is_correct = is_correct_input(user_input, text[0])

                key = stdscr.getch()

curses.wrapper(main)