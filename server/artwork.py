from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from glob import glob
from logging import info
from PIL import Image
from random import choice
from random import randint

from epd import DISPLAY_WIDTH
from epd import DISPLAY_HEIGHT

# The directory containing static artwork images.
IMAGES_DIR = "artwork"


def artwork_image():
    """Generates a random crop from a random artwork image."""

    # Load a random image.
    filename = choice(glob("%s/*.gif" % IMAGES_DIR))
    info("Using artwork file: %s" % filename)
    image = Image.open(filename)
    image = image.convert("RGB")

    # Crop the image to a random display-sized area.
    x = randint(0, max(0, image.size[0] - DISPLAY_WIDTH))
    y = randint(0, max(0, image.size[1] - DISPLAY_HEIGHT))
    image = image.crop((x, y, x + DISPLAY_WIDTH, y + DISPLAY_HEIGHT))

    return image
