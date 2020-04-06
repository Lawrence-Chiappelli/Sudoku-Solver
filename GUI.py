import pygame

# -------------+
pygame.init()  #
# -------------+

resolution = (1920, 1080)
caption = "Sudoku Puzzle"
bg_color = (255, 255, 255)
font_type, font_size = ('freesansbold.ttf', 115)


def text_objects(text, config):
    surface = config.render(text, True, (0, 0, 0))
    rectangle = surface.get_rect()
    return surface, rectangle


def display_text(text):
    font_size_config = pygame.font.Font(font_type, font_size)
    text_surface, text_rectangle = text_objects(text, font_size_config)
    text_rectangle.center = ((800//2), (600//2))
    window.blit(text_surface, text_rectangle)
    pygame.display.update()


window = pygame.display.set_mode(resolution)
window.fill(bg_color)
pygame.display.set_caption(caption)
display_text("Ultimate Suduoku Puzzles")

# ---------------------+
pygame.display.flip()  #
# ---------------------+


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
