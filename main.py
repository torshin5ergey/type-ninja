import curses
import time
import threading
import asyncio
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

def is_correct_input(user, task) -> bool:
    if user == task[:len(user)]:
        return True
    else:
        return False

def time_counter(stdscr, start:float):
    while True:
        remaining = round(timer - (time.time() - start))
        if remaining < 0:
            break
        ui.display_time(stdscr, remaining)
        time.sleep(.01)

def calculate_stats(typed_words, time, text):
    typed_text = " ".join(typed_words)
    typed_chars = len(typed_text)
    typed_words_count = len(typed_words)
    text_length = len(" ".join(text))

    wpm = round((typed_words_count / time) * 60)
    mistakes = sum(1 for i, j in zip(typed_text, ' '.join(text)) if i != j)
    accuracy = round(((typed_chars - mistakes) / typed_chars) * 100, 2)
    return wpm, accuracy, mistakes

def main(stdscr):
    global user_typed, text, is_correct, timer, task_typed
    # Main menu loop
    while True:
            # curses.curs_set(0)
            stdscr.clear()
            curses.curs_set(False)
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
                        ui.display_task(stdscr, user_input, user_typed, task_typed, text)
                        ui.display_user_input(stdscr, user_input, is_correct)
                        stdscr.refresh()
                        user_input = get_user_input(stdscr, user_input)
                        is_correct = is_correct_input(user_input, text[0])


                wpm, accuracy, mistakes = calculate_stats(user_typed, timer, task_typed)
                stdscr.addstr(10, 0, f'typed: {user_typed}, timer: {timer}, text: {task_typed}')
                stdscr.addstr(15, 0, f'WPM: {wpm}, Accuracy: {accuracy}%, Mistakes: {mistakes}')
                stdscr.refresh()
                key = stdscr.getch()


curses.wrapper(main)