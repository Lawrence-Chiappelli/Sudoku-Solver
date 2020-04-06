import pygame

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
blurple = (44, 47, 51)
font_type, font_size = ('freesansbold.ttf', 40)


class Button:

    def __init__(self, text, color, x_pos, y_pos, width, height):
        self.text = text
        self.color = color
        self.x = x_pos
        self.y = y_pos
        self.w = width
        self.h = height

    def draw(self, surface, outline=None):
        """
        Draws the button on the screen
        :param surface: the window/surface to draw on
        :param outline: outline color, if any
        """

        if outline:
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
window.fill(blurple)
pygame.display.set_caption(caption)
display_text("Ultimate Suduoku Puzzles")

button = Button("Click me!", red, resolution[0]//2, resolution[1]//2, 250, 100)
button.draw(window, black)

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.is_over(mouse_position):
                button.update_text("You clicked me!")

        if event.type == pygame.MOUSEMOTION:
            if button.is_over(mouse_position):
                button.update_color(green)
                button.update_text("Hovering!")
            else:
                button.update_color(red)
                button.update_text("Click me!")
