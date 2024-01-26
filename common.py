import random
import pygame
import os


MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
ASSETS_DIR = os.path.join(MAIN_DIR, "asset")


# helper function to help with ranges of values to randomly
# choose from (or do nothing if it's a value)
def resolve_range(t):
    if hasattr(t, "__getitem__"):
        if len(t) != 2:
            raise ValueError("Range %s contains more than 2 values" % str(t))
        if type(t[0]) is int:
            return random.randint(*t)
        elif type(t[0]) is float:
            lower = min(t)
            upper = max(t)
            return random.random() * (upper - lower) + lower
    # a scalar
    return t


def load_image(name):
    fullname = os.path.join(ASSETS_DIR, name)
    image = pygame.image.load(fullname).convert_alpha()
    image.set_colorkey(None)
    return image


# convert a grayscale + alpha image into an image
# in shades of a given color
def recolor_image(image, color):
    color = pygame.Color(color)
    a = pygame.surfarray.pixels2d(image)
    # TODO

