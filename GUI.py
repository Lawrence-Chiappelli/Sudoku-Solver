import pygame
from ButtonTxtRsc import TextResources

# -------------+
pygame.init()  #
# -------------+

resolution = (800, 800)
caption = "Sudoku Puzzle"
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
black = (0, 0, 0)
grey_discord = (44, 47, 51)
font_type, font_size = ('freesansbold.ttf', 40)


class Menu:

    def __init__(self):
        self.is_main_menu = True
        self.is_settings_menu = False
        self.is_game_screen = False

    def draw_main_menu(self):

        # MouseMotion events
        if event.type == pygame.MOUSEMOTION:
            if button_main.is_over(mouse_position):
                if button_main.text == txt_rsrcs.play:
                    button_main.update_color(green)
            else:
                button_main.update_color(red)
                button_main.update_text(txt_rsrcs.play)

            if button_settings.is_over(mouse_position):
                if button_settings.text == txt_rsrcs.settings:
                    button_settings.update_color(green)
            else:
                button_settings.update_color(red)
                button_settings.update_text(txt_rsrcs.settings)

        # MouseButtonDown events - load game screens here
        if event.type == pygame.MOUSEBUTTONDOWN:

            if button_main.is_over(mouse_position):
                self._load_game_menu()

            if button_settings.is_over(mouse_position):
                self._load_settings_menu()

    def draw_settings_menu(self):
        pass

    def draw_game_screen(self):
        tile1 = Button("", grey_discord, 10, 0, 80, 80)
        tile2 = Button("", grey_discord, tile1.x+85, 0, 80, 80)
        tile3 = Button("", grey_discord, tile2.x+85, 0, 80, 80)
        tile4 = Button("", grey_discord, tile3.x+85, 0, 80, 80)
        tile5 = Button("", grey_discord, tile4.x+85, 0, 80, 80)
        tile6 = Button("", grey_discord, tile5.x+85, 0, 80, 80)
        tile7 = Button("", grey_discord, tile6.x+85, 0, 80, 80)
        tile8 = Button("", grey_discord, tile7.x+85, 0, 80, 80)
        tile9 = Button("", grey_discord, tile8.x+85, 0, 80, 80)
        tile1.draw(window)
        tile2.draw(window)
        tile3.draw(window)
        tile4.draw(window)
        tile5.draw(window)
        tile6.draw(window)
        tile7.draw(window)
        tile8.draw(window)
        tile9.draw(window)


    def _load_main_menu(self):
        pass

    def _load_settings_menu(self):
        self.is_main_menu = False
        self.is_settings_menu = True
        self.is_game_screen = False
        button_settings.update_color(blue)
        button_settings.update_text(txt_rsrcs.clicked)

    def _load_game_menu(self):
        self.is_main_menu = False
        self.is_settings_menu = False
        self.is_game_screen = True
        window.fill(white)
        pygame.display.flip()


class Button:

    def __init__(self, text, color, x_pos, y_pos, width, height):
        self.text = text
        self.color = color
        self.x = x_pos
        self.y = y_pos
        self.w = width
        self.h = height

    def draw(self, surface, outline=None, xcenter=False):
        """
        Draws the button on the screen
        :param surface: the window/surface to draw on
        :param outline: outline color, if any
        :param xcenter: center this button on the x-axis? No by default
        """
        if xcenter:
            self.x = (surface.get_width() // 2) - (self.w // 2) - 4

        if outline:
            # x = self.x-4
            x = self.x-4
            y = self.y-4
            w = self.w+8
            h = self.h+8
            pygame.draw.rect(surface, outline, (x, y, w, h), 0)

        pygame.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, white)
            center = (self.x + (self.w//2 - text.get_width()//2), self.y + (self.h//2 - text.get_height()//2))
            surface.blit(text, center)

        # -----------------------+
        pygame.display.update()  #
        # -----------------------+

    def is_over(self, position):
        if self.x < position[0] < self.x + self.w:
            if self.y < position[1] < self.y + self.h:
                return True
        return False

    def update_color(self, color):
        self.color = color
        self.draw(window, black)

    def update_text(self, text):
        self.text = text
        self.draw(window, black)


def text_objects(text, config):
    surface = config.render(text, True, white)
    rectangle = surface.get_rect()
    return surface, rectangle


def display_text(text):
    font_size_config = pygame.font.Font(font_type, font_size)
    text_surface, text_rectangle = text_objects(text, font_size_config)
    text_rectangle.center = ((800//2), 100)
    window.blit(text_surface, text_rectangle)
    pygame.display.update()


window = pygame.display.set_mode(resolution)
window.fill(grey_discord)
pygame.display.set_caption(caption)
display_text("Ultimate Suduoku Puzzles")
txt_rsrcs = TextResources()

button_main = Button(txt_rsrcs.play, red, window.get_width() // 2, window.get_height() // 2, 250, 100)
button_main.draw(window, black, True)
button_settings = Button(txt_rsrcs.settings, grey_discord, window.get_width() // 2, (window.get_height() // 2) + 150, 250, 100)
button_settings.draw(window, black, True)

menu = Menu()


# ---------------------+
pygame.display.flip()  #
# ---------------------+


running = True
while running:

    for event in pygame.event.get():

        mouse_position = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()  # TODO: Some people recommend this. Necessary?
            quit()  # And why this?

        if menu.is_main_menu:
            menu.draw_main_menu()
        elif menu.is_game_screen:
            menu.draw_game_screen()
        elif menu.is_settings_menu:
            menu.draw_settings_menu()
        else:
            running = False
            pygame.quit()
            quit()

