import curses, _curses, sys, os, time

class MenuOption:
    '''
    Supplement class for the MenuInterface, makes presenting options easier
    '''
    def __init__(self, content: str, callback, height: int = 0, width: int = 0):
        self.id = None
        self.height = height
        self.width = width
        self.content = content
        self.selected = False
        self.callback = callback


class Interface:
    '''
    Generic class for UI elements
    '''
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
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        screen.clear()
        self.draw()


    def display_location_info(self, data: dict, heading: str)->None:
        self.screen.clear()
        self.draw()
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
    #TODO: Improve the presentation of this element, maybe center it and have columns
    '''
    Subclass to display data retrieved from the API
    '''
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
        self.screen.refresh()

    def draw_info(self):
        self.draw()
        self.populate()


class MenuInterface (Interface):
    def __init__(self, parent: MainInterface, heading: str = "")->None:
        #TODO: Figure out if this should be defined explicitly or calculated
        self.height = 3
        self.width = 20
        self.anchor_y = 3
        self.anchor_x = (parent.width // 2) - (self.width // 2)

        # Creates a new window centered in the parent window
        new_screen = curses.newwin(self.height, self.width, self.anchor_y, self.anchor_x)
        super().__init__(screen=new_screen, parent=parent)
        self.options = []
        self.option_height = 3

        # Defines the anchor point for menu options
        self.option_y = 1
        self.option_x = 1

        self.heading = heading


    def resize_for_options(self):
        option_width = max(len(self.heading) + 2, max([i.width for i in self.options]))
        self.width = option_width + 3
        for i, o in enumerate(self.options):
            o.width = option_width
        self.screen.resize(self.height, self.width)


    def add_option(self, option: MenuOption)->None:
        option.id = len(self.options)
        option.height = self.option_height
        option.width = len(option.content) + 2
        self.options.append(option)
        self.height += self.option_height
        self.resize_for_options()


    def draw_options(self):
        cx = self.option_x
        cy = self.option_y
        for option in self.options:
            if option.selected:
                self.screen.attron(curses.color_pair(2))
            else:
                self.screen.attroff(curses.color_pair(2))

            # Draws top of box
            self.screen.addch(cy, cx, self.ul_corner)
            for i in range(option.width - 1):
                self.screen.addch(self.horizontal)
            self.screen.addch(self.ur_corner)
            cy += 1

            # Draws middle of box
            self.screen.addch(cy, cx, self.vertical)
            self.screen.addstr(option.content.center(option.width - 1))
            self.screen.addch(self.vertical)
            cy += 1

            # Draws bottom of box
            self.screen.addch(cy, cx, self.bl_corner)
            for i in range(option.width - 1):
                self.screen.addch(self.horizontal)
            self.screen.addch(self.br_corner)
            self.screen.refresh()
            cy += 1


    def get_selection(self, log = None):
        k = ''
        selected = [i for i in self.options if i.selected][0]
        self.screen.keypad(True)
        while k != ord('c'):
            k = self.screen.getch()
            if k == curses.KEY_DOWN:
                if selected.id < len(self.options) - 1:
                    id = selected.id
                    self.options[id].selected = False
                    self.options[id + 1].selected = True
                    selected = self.options[id + 1]
            if k == curses.KEY_UP:
                if selected.id > 0:
                    id = selected.id
                    self.options[id].selected = False
                    self.options[id - 1].selected = True
                    selected = self.options[id - 1]
            if k == ord('\n'):
                if log != None:
                    log.write(selected.content)
                self.screen.clear()
                self.screen.refresh()
                selected.callback()
                break
            self.draw_options()
        self.screen.clear()
        self.screen.refresh()
