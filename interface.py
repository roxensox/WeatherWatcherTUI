import sys,os
import _curses, curses


def main_interface(stdscr: _curses.window):
    k = ''
    mainscreen = MainInterface(screen=stdscr)
    mainscreen.draw()
    location = mainscreen.get_location()
    #mainscreen.screen.addstr(10, 10, location)
    mainscreen.draw()
    while k != ord('q'):
        if curses.is_term_resized(mainscreen.height, mainscreen.width):
            mainscreen.resize_handler()
        k = stdscr.getch()


class Interface:
    def __init__(self, screen: _curses.window, y: int =0, x: int =0, parent = None)->None:
        self.screen = screen
        max_y, max_x = screen.getmaxyx()
        self.height = max_y
        self.width = max_x
        self.anchor_y = y
        self.anchor_x = x
        self.parent = parent

        # These are declared inside of the class so they can be 
        # modified / cleared in inheriting classes
        self.ul_corner = '\u250C'
        self.ur_corner = '\u2510'
        self.vertical = '\u2502'
        self.horizontal = '\u2500'
        self.bl_corner = '\u2514'
        self.br_corner = '\u2518'


    def resize_handler(self):
        if self.parent is None:
            curses.update_lines_cols()
            newy, newx = self.screen.getmaxyx()
            curses.resizeterm(newy, newx)
            self.screen.resize(newy, newx)
            self.height, self.width = newy, newx
        else:
            newy, newx = self.screen.getmaxyx()
            curses.resizeterm(newy, newx)
            self.height, self.width = newy, newx
            self.screen = curses.newwin(self.height, self.width, 0, 0)
        self.screen.clear()
        self.draw()


    def draw(self)->None:
        '''
        Draws a box for the perimeter of the interface
        '''
        cy, cx = self.anchor_y, 0
        self.screen.addch(cy, cx, self.ul_corner)
        for i in range(1, self.width - 1):
            self.screen.addch(cy, cx + i, self.horizontal)
        self.screen.addch(cy, self.width - 1, self.ur_corner)
        cy += 1
        while cy < self.height - 2:
            self.screen.addch(cy, cx, f"{self.vertical}")
            self.screen.addch(cy, self.width - 1, f"{self.vertical}")
            cy += 1
        self.screen.addch(cy,cx,self.bl_corner)
        for i in range(1, self.width - 1):
            self.screen.addch(cy, cx + i, self.horizontal)
            self.screen.refresh()
        self.screen.addch(cy, self.width - 1, self.br_corner)
        self.screen.refresh()


    def get_string(self, leftBound: int, cy: int)->str:
        '''
        Gets user input string
        '''
        string = ""
        k = ''
        cx = leftBound

        # This calculates the max length of the string
        # which shouldn't extend past the box
        max_length = self.width - leftBound - 3

        while k != '\n':
            if curses.is_term_resized(self.parent.height, self.parent.width):
                self.resize_handler()
                continue
            k = self.screen.getch()
            self.parent.screen.addstr(10,10,chr(k))
            self.parent.screen.refresh()
            if chr(k) == '\u001B' or chr(k) == '\n':
                break

            # 127 is the backspace key
            if k == 127:
                if len(string) > 0:
                    string = string[:-1]
                self.screen.addstr(cy, leftBound, ' ' * (self.width - leftBound - 1))
                if cx > leftBound:
                    cx -= 1
            else:
                if len(string) <= max_length:
                    string += chr(k)

            self.screen.addstr(cy,leftBound,string)
            self.screen.refresh()
        return string


class MainInterface (Interface):
    '''
    Represents the main interface for the app, should take up the entire terminal
    '''
    def __init__(self, screen: _curses.window)->None:
        super().__init__(screen)
        curses.use_default_colors()
        curses.curs_set(1)
        curses.meta(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        screen.clear()


    def get_location(self)->str:
        '''
        Prompts the user for location input and returns it as a string
        '''
        # Arguments here are arbitrary, can be modified to taste
        location_window = self.make_window(5, 50, 1, 2)
        location_window.draw()
        # The coordinates here will depend on arguments to make_window; it just centers the text
        location_window.screen.addstr(location_window.height // 2, 1, "Set Location: ")
        location_window.screen.refresh()
        lbound = len("Set Location: ") + 1
        string = location_window.get_string(leftBound=lbound, cy=location_window.height // 2)
        location_window.screen.clear()
        location_window.screen.refresh()
        return string


    def make_window(self, height: int, width: int, y: int, x: int):
        return Interface(screen=curses.newwin(height, width, y, x), y=y, x=x, parent=self)


class InfoInterface (Interface):
    def __init__(self, screen: _curses.window, data: dict)->None:
        super().__init__(screen)
        self.data = data


def main():
    curses.wrapper(main_interface)

if __name__ == "__main__":
    main()
