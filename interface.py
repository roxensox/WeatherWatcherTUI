import sys,os
import _curses, curses


def main_interface(stdscr):
    k = ''
    mainscreen = MainInterface(stdscr)
    mainscreen.draw()
    location = mainscreen.get_location()
    mainscreen.screen.addstr(10, 10, location)
    while k != ord('q'):
        k = stdscr.getch()


class Interface:
    def __init__(self, screen):
        self.screen = screen
        y, x = screen.getmaxyx()
        self.height = y
        self.width = x

        # These are declared inside of the class so they can be 
        # modified / cleared in inheriting classes
        self.ul_corner = '\u250C'
        self.ur_corner = '\u2510'
        self.vertical = '\u2502'
        self.horizontal = '\u2500'
        self.bl_corner = '\u2514'
        self.br_corner = '\u2518'


    def draw(self):
        '''
        Draws a box for the perimeter of the interface
        '''
        cy, cx = 0, 0
        self.screen.addstr(cy,cx,f"{self.ul_corner}")
        for i in range(self.width - 2):
            self.screen.addstr(f"{self.horizontal}")
            self.screen.refresh()
        self.screen.addstr(f"{self.ur_corner}")
        cy += 1
        while cy < self.height - 2:
            self.screen.addstr(cy, cx, f"{self.vertical}{' ' * (self.width - 2)}{self.vertical}")
            cy += 1
        self.screen.addstr(cy,cx,f"{self.bl_corner}")
        for i in range(self.width - 2):
            self.screen.addstr(f"{self.horizontal}")
            self.screen.refresh()
        self.screen.addstr(f"{self.br_corner}")
        self.screen.refresh()


    def get_string(self, leftBound, cy)->str:
        '''
        Gets user input string
        '''
        string = ""
        k = ''
        cx = leftBound
        while k != '\n':
            k = self.screen.getkey()
            if k == '\u001B' or k == '\n':
                break
            if ord(k) == 127:
                if len(string) > 0:
                    string = string[:-1]
                self.screen.addstr(cy, leftBound, ' ' * (self.width - leftBound - 1))
                self.screen.addstr(cy, leftBound, string)
                if cx > leftBound:
                    cx -= 1
            else:
                self.screen.addstr(cy,cx,k)
                if cx < self.width - 3:
                    string += k
                    cx += 1
            self.screen.refresh()
        return string


class MainInterface (Interface):
    def __init__(self, screen):
        super().__init__(screen)
        curses.use_default_colors()
        curses.curs_set(1)
        curses.meta(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        screen.clear()


    def get_location(self):
        '''
        Prompts the user for location input and returns it as a string
        '''
        # Arguments here are arbitrary, can be modified to taste
        location_window = self.make_window(4, 50, 1, 2)
        location_window.draw()
        # The coordinates here will depend on arguments to make_window; it just centers the text
        location_window.screen.addstr(1, 1, "Set Location: ")
        location_window.screen.refresh()
        lbound = 1 + len("Set Location: ")
        string = location_window.get_string(leftBound=lbound, cy=1)
        location_window.screen.clear()
        location_window.screen.refresh()
        return string


    def make_window(self, height, width, y, x):
        return Interface(curses.newwin(height, width, y, x))


def main():
    curses.wrapper(main_interface)

if __name__ == "__main__":
    main()
