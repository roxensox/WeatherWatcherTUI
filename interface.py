import sys,os
import _curses, curses

ul_corner = '\u250C'
ur_corner = '\u2510'
vertical = '\u2502'
horizontal = '\u2500'
bl_corner = '\u2514'
br_corner = '\u2518'


def get_location(width: int, height: int)->str:
    '''
    Creates a menu to enter a location
    '''
    screen = curses.newwin(height, width, 1, 2)
    coordx = 0
    coordy = 0
    draw_box(screen, width, height, coordy, coordx)
    coordx = 1
    coordy = (height - 2) // 2
    screen.addstr(coordy, coordx, "Set Location: ")
    coordx += len("Set Location: ")
    screen.refresh()
    return get_string(screen, coordx, coordy, coordx)


def draw_box(screen, width: int, height: int, cy: int, cx: int)->None:
    '''
    Draws a box with the given dimensions on the given screen.
    THIS WORKS IN GHOSTTY
    '''
    screen.addstr(cy,cx,f"{ul_corner}")
    for i in range(width - 2):
        screen.addstr(f"{horizontal}")
        screen.refresh()
    screen.addstr(f"{ur_corner}")
    cy += 1
    while cy < height - 2:
        screen.addstr(cy, cx, f"{vertical}{' ' * (width - 2)}{vertical}")
        cy += 1
    screen.addstr(cy,cx,f"{bl_corner}")
    for i in range(width - 2):
        screen.addstr(f"{horizontal}")
        screen.refresh()
    screen.addstr(f"{br_corner}")


def get_string(screen, leftBound, cy, cx)->str:
    '''
    Gets user input string
    '''
    string = ""
    k = ''
    height, width = screen.getmaxyx()
    while k != '\n':
        k = screen.getkey()
        if k == '\u001B' or k == '\n':
            break
        if ord(k) == 127:
            if len(string) > 0:
                string = string[:-1]
            screen.addstr(cy, leftBound, ' ' * (width - leftBound - 1))
            screen.addstr(cy, leftBound, string)
            if cx > leftBound:
                cx -= 1
        else:
            screen.addstr(cy,cx,k)
            if cx < width - 3:
                string += k
                cx += 1
        screen.refresh()
    return string


def main_interface(stdscr):
    k = ''
    curses.use_default_colors()
    curses.curs_set(1)
    curses.meta(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    stdscr.clear()
    location = get_location(50, 4)
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    coordx = 0
    coordy = 0
    draw_box(stdscr, width, height, coordy, coordx)
    coordx = 1
    coordy = 1
    stdscr.addstr(coordy, coordx, '')
    stdscr.addstr(1,1,f"Location: {location}")
    stdscr.refresh()
    while k != ord('q'):
        k = stdscr.getch()


def main():
    curses.wrapper(main_interface)

if __name__ == "__main__":
    main()
