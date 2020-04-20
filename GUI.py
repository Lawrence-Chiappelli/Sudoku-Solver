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
        self.main_menu = True
        self.settings = False
        self.game = False


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

current_menu = Menu()


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

        if current_menu.main_menu:
            if event.type == pygame.MOUSEBUTTONDOWN:  # MouseButtonDown

                if button_main.is_over(mouse_position):
                    if button_main.text == txt_rsrcs.play:
                        window.fill(grey_discord)
                        pygame.display.flip()
                        current_menu.main_menu = False
                        current_menu.game = True

                if button_settings.is_over(mouse_position):
                    if button_settings.text == txt_rsrcs.settings:
                        button_settings.update_color(blue)
                        button_settings.update_text(txt_rsrcs.clicked)

            if event.type == pygame.MOUSEMOTION:  # MouseMotion
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
        elif current_menu.settings:
            print(f"Went to settings!")
        elif current_menu.game:
            print(f"Went to game!")
