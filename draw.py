import pygame as pg


BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
NAVAJO_WHITE = [255, 222, 173]
SKY_BLUE = [163, 229, 255]
SAND_YELLOW = [249, 197, 17]
PERU_BROWN = [205, 133, 63]


class Drawer:

    def __init__(self, screen, screen_width, current_level):
        """
        Initializes a Drawer-object for drawing Levels.

        :param screen: Pygame display
        :param screen_width: width of display
        :param current_level: Level-object that needs to be drawn
        """
        self.screen = screen
        self.width = screen_width
        self.level = current_level
        self.pos, self.radius = self.update_positions()

    def draw_level(self, font, background, min_moves, buttons, animation):
        """
        Intermediary function which calls all required functions for drawing a Level.

        :param font: font already loaded from resources
        :param background: wallpaper image already loaded from resources
        :param min_moves: minimum number of moves required for solution
        :param buttons: dict consisting of Rect-objects corresponding to button-text
        :param animation: bool that indicates whether function is called for animation
        """
        self.screen.fill(WHITE)
        self.screen.blit(background, background.get_rect())     # Draws background image

        # Animation-functions update positions independently
        if not animation:
            self.pos, self.radius = self.update_positions()

        self.draw_circles(self.pos, self.radius)
        self.draw_buttons(font, buttons)
        self.draw_counter(font, min_moves)

    def draw_circles(self, pos, radius):
        """
        Draws the circles of the Level's circles-list

        :param pos: dict consisting of coordinates for each circle
        :param radius:  radius of the circles
        """
        for circle in pos:
            pg.draw.circle(self.screen, self.level.colors[circle], pos[circle], radius)

    def update_positions(self):
        """
        Calculates the position and radius of each circle from the Level.

        :return: dict consisting of coordinates for each circle; the radius of the circles
        """
        n_circles = len(self.level.circles)
        center = self.width / 2
        space = 15  # Space in between circles, must be dividable by 5

        # Let radius be as big as possible but no bigger than 50 pixels
        # Radius must be dividable by 5 in order for animations to work properly
        radius = min(50, int((self.width - space * (n_circles + 1)) / (2 * n_circles)) // 5 * 5)

        ycor = 180
        # Gets xcor for the leftmost circle
        if len(self.level.circles) % 2 == 0:    # Even number of circles
            xcor = int(center - (space / 2 + (n_circles / 2 - 1) * (2 * radius + space) + radius))
        else:
            xcor = int(center - (((n_circles - 1) / 2) * (2 * radius + space)))

        # Store coordinates for each circle in dict
        pos = dict()
        for circle in self.level.circles:
            pos[circle] = xcor, ycor
            xcor += (2 * radius + space)    # xcor for the circle to the right

        return pos, radius

    def draw_buttons(self, font, buttons):
        """
        Draws each button on the screen.

        :param font: font already loaded from resources
        :param buttons: dict consisting of Rect-objects corresponding to button-text
        """
        for text, button in buttons.items():
            pg.draw.rect(self.screen, SKY_BLUE, button)

            # Get corresponding text on the button
            pos_x, pos_y = button.center
            text_width, text_height = font.size(text)
            position = pos_x - (text_width / 2), pos_y - (text_height / 2)
            writing = font.render(text, True, [0, 0, 0])
            self.screen.blit(writing, position)

    def draw_message(self, font, text):
        """
        Helper function that draws the headline on the screen when Level is solved.

        :param font: font already loaded from resources
        :param text: string that needs to be printed on the screen
        """
        center = self.width / 2
        text_width, text_height = font.size(text)
        writing = font.render(text, True, BLACK, SAND_YELLOW)
        self.screen.blit(writing, (center - text_width / 2, text_height + 10))

    def draw_counter(self, font, min_moves):
        """
        Draws counter-text that keeps track of the number of moves / minimum required.

        :param font: font already loaded from resources
        :param min_moves: minimum number of moves required for solution
        """
        text = "Moves:  " + str(self.level.counter) + " (" + str(min_moves) + ")"
        text_width, text_height = font.size(text)
        written = font.render(text, True, BLACK, SAND_YELLOW)
        self.screen.blit(written, (self.width / 2 - text_width / 2, 350))

    def animate_ab(self, font, background, min_moves, buttons, action):
        """
        Animates the swapping movement performed when action a or b is executed.

        :param font: font already loaded from resources
        :param background: wallpaper image already loaded from resources
        :param min_moves: minimum number of moves required for solution
        :param buttons: dict consisting of Rect-objects corresponding to button-text
        :param action: string indication the action to animate, a or b
        """
        self.pos, self.radius = self.update_positions()

        # Gets the two circles corresponding to the action
        if action == 'a':
            first = self.level.circles[0]
            second = self.level.circles[1]
        else:
            first = self.level.circles[-2]
            second = self.level.circles[-1]

        # Stores their location
        x1, y1 = self.pos[first]
        x2, y2 = self.pos[second]
        old_x2 = x2

        while x1 < old_x2:  # Terminates when circle 1 has passed circle 2's old position
            # Slightly move the circles on the x-axis
            x1 += 5
            self.pos[first] = x1, y1
            x2 -= 5
            self.pos[second] = x2, y2

            # Redraw the Level with updated positions
            self.draw_level(font, background, min_moves, buttons, animation=True)
            pg.display.update()
            pg.time.delay(1)    # So that the animation is not too fast

    def animate_x(self, font, background, min_moves, buttons):
        """
        Animates the shifting movement performed when action x is executed.

        :param font: font already loaded from resources
        :param background: wallpaper image already loaded from resources
        :param min_moves: minimum number of moves required for solution
        :param buttons: dict consisting of Rect-objects corresponding to button-text
        """
        self.pos, self.radius = self.update_positions()

        # Calculate factor for difference in distance for rightmost middle circle
        faster = len(self.level.circles) - 3

        # Get position of leftmost and rightmost middle circles
        first = self.level.circles[1]
        last = self.level.circles[-2]
        old_x_first1, old_y_first1 = self.pos[first]
        x_last, y_last = self.pos[last]

        while x_last > old_x_first1:    # Terminates when last circle has passed first circle's old position

            # Slightly move the middle circles to the right on the x-axis
            # With the exception of the rightmost middle circle
            for i in range(1, len(self.level.circles) - 2):
                circle_number = self.level.circles[i]
                x1, y1 = self.pos[circle_number]
                self.pos[circle_number] = x1 + 5, y1

            # Move the rightmost middle circle to the left on the x-axis
            # Takes difference in traveling distance into account
            x_last, y_last = self.pos[last]
            x_last -= 5 * faster
            self.pos[last] = x_last, y_last

            # Redraw the Level with updated positions
            self.draw_level(font, background, min_moves, buttons, animation=True)
            pg.display.update()
            pg.time.delay(1)

    def draw_solved(self, font, text):
        """
        Draws the solved-screen for when a level is finished.

        :param font: font already loaded from resources
        :param text: string that needs to be printed on the screen
        """
        # Create buttons for solved-screen
        button_width = 200
        button_height = 50
        button_retry = pg.Rect(self.width / 2 - button_width, 250, button_width, button_height)
        button_next = pg.Rect(self.width / 2, 250, button_width, button_height)
        buttons = {'Retry': button_retry, 'Next': button_next}

        self.draw_message(font, text)
        self.draw_buttons(font, buttons)

        # Hide the buttons on the top of the screen
        cover_buttons = pg.Rect(0, 0, self.width, 50)
        pg.draw.rect(self.screen, SKY_BLUE, cover_buttons)

        pg.display.update()

        new_level = False   # Indicates whether a new game needs to be started

        done = False
        while not done:
            for event in pg.event.get():

                # Quit when exit-button is clicked
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos  # Gets mouse position

                    # Retry button is clicked
                    if button_retry.collidepoint(mouse_x, mouse_y):
                        done = True

                    # Next button is clicked, which will cause a new game to start
                    if button_next.collidepoint(mouse_x, mouse_y):
                        new_level = True
                        done = True

        return new_level

    def show_help(self):
        """ Draw a info/help-window containing the game's explanation. """

        # Draw window
        window = pg.Rect(self.width / 2 - 180, 40, 360, 350)
        pg.draw.rect(self.screen, NAVAJO_WHITE, window)
        pg.draw.rect(self.screen, PERU_BROWN, window, 5)

        # Game explanation
        text = " TRICKY CIRCLES GAME EXPLANATION \n \n" \
               " The goal of this game is to get the \n colored circles in the right order:\n" \
               " from red (left) to violet (right), like a rainbow. \n \n" \
               " A: swap the first two circles \n" \
               " B: swap the last two circles \n" \
               " X: shift the circles in the middle \n \n" \
               " MOVES: number of actions executed \n" \
               " (and minimum number of moves required) \n \n" \
               " SOLVE: computer auto-solves the level \n" \
               " RESET: level restarts in the begin-order \n" \
               " +: adds a circle, max 8 (increases difficulty) \n" \
               " -: removes a circle, min 4 (decreases difficulty) \n"

        lines = text.splitlines()
        font_size = int(window.height / len(lines))
        font = pg.font.SysFont("Arial", font_size)
        x, y = window.topleft

        # Print each line onto the screen
        for i, l in enumerate(lines):
            self.screen.blit(font.render(l, 0, BLACK), (x, y + font_size * i))

        pg.display.update()

        while True:
            for event in pg.event.get():

                # Quits when exit-button is clicked
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos  # Get mouse position

                    # Click anywhere except on the window to close it
                    if not window.collidepoint(mouse_x, mouse_y):
                        return False
