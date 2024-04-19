import curses
import time
import ui
import bs4

def get_random_wikipedia_article():
    text = 'Endozoicomonas elysicola is a Gram-negative, rod-shaped and strictly aerobic bacterium from the genus of Endozoicomonas which has been isolated from the gastrointestinal tract of the sea slug Elysia ornata from the coast of Izu-Miyake Island in Japan.'
    pass

def main(stdscr):
    
    # curses.curs_set(0)
    stdscr.clear()

    # Menu
    ui.get_window_size(stdscr)
    ui.display_menu(stdscr)

    stdscr.refresh()

    # Main menu loop
    while True:
        key = stdscr.getch()
        if key == 24:
            break
        elif key == 18:
            get_random_wikipedia_article()
            start_time = time.time()

curses.wrapper(main)