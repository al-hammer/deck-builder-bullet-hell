from common import *
import pygame
import numpy


RED = pygame.Color(255, 0, 0)
ORANGE = pygame.Color(255, 165, 0)
YELLOW = pygame.Color(255, 255, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
INDIGO = pygame.Color(75, 0, 130)
VIOLET = pygame.Color(238, 130, 238)
BLACK = pygame.Color(0, 0, 0)
TRANSPARENT = pygame.Color(0, 0, 0, 0)

RAINBOW = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET]


def load_image(name):
    fullname = os.path.join(ASSETS_DIR, name)
    image = pygame.image.load(fullname).convert_alpha()
    image.set_colorkey(None)
    return image


# convert a grayscale + alpha image into an image
# in shades of a given color
def recolor_image(image, color):
    color = pygame.Color(color)
    recolored_image = image.copy()

    pixels_red = pygame.surfarray.pixels_red(recolored_image)
    # 'unsafe' here means you can lose information in the cast
    numpy.multiply(pixels_red, color.r / 255, out=pixels_red, casting='unsafe')

    pixels_green = pygame.surfarray.pixels_green(recolored_image)
    numpy.multiply(pixels_green, color.g / 255, out=pixels_green, casting='unsafe')

    pixels_blue = pygame.surfarray.pixels_blue(recolored_image)
    numpy.multiply(pixels_blue, color.b / 255, out=pixels_blue, casting='unsafe')

    return recolored_image

