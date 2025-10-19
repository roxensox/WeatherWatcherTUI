import sys,os,time
import _curses, curses
import processing as p

LAST_REFRESHED = time.time()

def main_interface(stdscr: _curses.window, cfg):
    wp = p.WeatherProcessor()
    k = ''
    mainscreen = MainInterface(screen=stdscr)
    mainscreen.draw()
    mainscreen.screen.nodelay(True)
    rd = get_valid_location(cfg, mainscreen)
    data = wp.load_data(rd)
    mainscreen.display_location_info(data=wp.filtered_data, heading="Weather")
    LAST_REFRESHED = time.time()
    refresh_interval = 5
    data = wp.load_data(cfg.get_weather())
    mainscreen.display_location_info(data=wp.filtered_data, heading="Weather")
    mainscreen.screen.move(mainscreen.height - 1, 0)
    while k != ord('q'):
        k = mainscreen.screen.getch()
        if curses.is_term_resized(mainscreen.height, mainscreen.width):
            mainscreen.resize_handler()
        now = time.time()
        if now - LAST_REFRESHED >= refresh_interval:
            data = wp.load_data(cfg.get_weather())
            mainscreen.display_location_info(data=wp.filtered_data, heading="Weather")
            LAST_REFRESHED = now
        if k == ord('r'):
            mainscreen.screen.clear()
            mainscreen.screen.refresh()
            mainscreen.draw()
            rd = get_valid_location(cfg, mainscreen)
            data = wp.load_data(rd)
            mainscreen.display_location_info(data=wp.filtered_data, heading="Weather")
            LAST_REFRESHED = now
        time.sleep(0.05)


def get_valid_location(cfg, main):
    '''
    Prompts for input and validates it with the API
    '''
    rough_data = {}
    while rough_data.get("location") == None:
        location = main.get_location()
        main.screen.addstr(1, 1, location)
        main.draw()
        cfg.set_location(location)
        rough_data = cfg.get_weather()
    return rough_data



class Interface:
    def __init__(self, screen: _curses.window, y: int =0, x: int =0, parent = None, heading: str = "")->None:
        self.screen = screen
        max_y, max_x = screen.getmaxyx()
        self.original_width = max_x
        self.height = max_y
        self.width = max_x
        self.anchor_y = y
        self.anchor_x = x
        self.parent = parent
        self.heading = heading
        self.children = []

        # These are declared inside of the class so they can be 
        # modified / cleared in inheriting classes
        self.ul_corner = '\u250C'
        self.ur_corner = '\u2510'
        self.vertical = '\u2502'
        self.horizontal = '\u2500'
        self.bl_corner = '\u2514'
        self.br_corner = '\u2518'


    def resize_handler(self):
        '''
        Resizes windows when the terminal is resized
        '''

        LAST_REFRESHED = time.time() - 20

        # Handler for the main window
        if self.parent is None:
            curses.update_lines_cols()
            newy, newx = self.screen.getmaxyx()
            curses.resizeterm(newy, newx)
            self.screen.resize(newy, newx)
            self.height, self.width = newy, newx
            self.screen.clear()
            self.draw()
        # Handler for all sub-windows
        else:
            #self.parent.resize_handler()
            parent_y, parent_x = self.parent.height, self.parent.width
            new_height = min(self.height, parent_y - self.anchor_y - 1)
            new_width = min(self.width, parent_x - self.anchor_x - 1)
            if parent_x > self.original_width + 2:
                new_width = self.original_width

            try:
                self.screen = curses.newwin(
                    new_height,
                    new_width,
                    self.anchor_y,
                    self.anchor_x,
                )
                self.height, self.width = new_height, new_width
                self.screen.clear()
                self.draw()
            except curses.error:
                pass


    def draw(self)->None:
        cy = 0
        self.screen.addch(cy, 0, self.ul_corner)
        self.screen.addstr(self.heading)
        for i in range(len(self.heading) + 1, self.width - 1):
            self.screen.addch(cy,i,self.horizontal)
        self.screen.addch(cy, self.width - 1, self.ur_corner)
        while cy < self.height - 2:
            cy += 1
            self.screen.addch(cy, 0, self.vertical)
            #self.screen.addstr(cy, 1, f"{cy}")
            self.screen.addch(cy, self.width - 1, self.vertical)
        self.screen.addch(cy, 0, self.bl_corner)
        for i in range(1, self.width - 1):
            self.screen.addch(cy,i,self.horizontal)
        self.screen.addch(cy, self.width - 1, self.br_corner)
        self.screen.refresh()


    def get_string(self, leftBound: int, cy: int, prompt: str = "")->str:
        '''
        Gets user input string
        '''
        string = ""
        k = -1
        cx = leftBound

        # This calculates the max length of the string
        # which shouldn't extend past the box
        max_length = self.width - leftBound - 3

        while k != '\n':
            self.screen.addstr(cy,1, prompt + string)
            self.screen.refresh()
            if curses.is_term_resized(self.parent.height, self.parent.width):
                self.resize_handler()
                continue
            k = self.screen.getch()

            # Curses reads a resize as this character, so it's skipped
            if chr(k) == 'ƚ':
                continue

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


    def display_location_info(self, data: dict, heading: str)->None:
        screen = curses.newwin(len(data) + 3, max([len(": ".join(i)) for i in data]) + 2, 1, 1)
        infoScreen1 = InfoInterface(screen=screen, data=data, heading=heading, parent=self)
        infoScreen1.draw_info()
        self.screen.move(self.height - 1, 0)
        self.children.append(infoScreen1)


    def get_location(self)->str:
        '''
        Prompts the user for location input and returns it as a string
        '''
        # Arguments here are arbitrary, can be modified to taste
        location_window = self.make_window(4, 50, 1, 1)
        location_window.draw()
        # The coordinates here will depend on arguments to make_window; it just centers the text
        location_window.screen.refresh()
        prompt = "Set Location: "
        lbound = len(prompt) + 1
        string = location_window.get_string(leftBound=lbound, cy=1, prompt=prompt)
        location_window.screen.clear()
        location_window.screen.refresh()
        return string


    def make_window(self, height: int, width: int, y: int, x: int):
        return Interface(screen=curses.newwin(height, width, y, x), y=y, x=x, parent=self)


class InfoInterface (Interface):
    def __init__(self, screen: _curses.window, data: list, heading: str, parent: MainInterface)->None:
        super().__init__(screen)
        self.data = data
        self.heading = heading

    def populate(self):
        cy = 1
        cx = 1
        for k in self.data:
            self.screen.addstr(cy, cx, f"{k[0]}:")
            self.screen.addstr(cy, self.width - len(k[1]) - 1, f"{k[1]}")
            cy += 1
        curses.curs_set(0)
        self.screen.refresh()

    def draw_info(self):
        self.draw()
        self.populate()
